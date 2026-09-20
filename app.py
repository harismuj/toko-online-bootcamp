import sqlite3
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = "toko_online.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Hasil query berbentuk dictionary
    return conn


def init_db():
    with app.app_context():
        db = get_db()
        with open("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


# Rute Halaman utama untuk menyajikan UI
@app.route("/")
def home():
    return render_template("index.html")


# 1. Rute /api/produk (GET: Ambil semua produk, POST: Tambah produk baru)
@app.route("/api/produk", methods=["GET", "POST"])
def manage_produk():
    db = get_db()

    if request.method == "POST":
        data = request.get_json()
        nama = data.get("nama")
        harga = data.get("harga")
        stok = data.get("stok")

        if not nama or harga is None or stok is None:
            return (
                jsonify({"error": "Data nama, harga, dan stok wajib diisi"}),
                400,
            )

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)",
            (nama, harga, stok),
        )
        db.commit()

        return (
            jsonify(
                {
                    "message": "Produk berhasil ditambahkan",
                    "id": cursor.lastrowid,
                }
            ),
            201,
        )

    # Method GET
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produk")
    produk_list = [dict(row) for row in cursor.fetchall()]
    return jsonify(produk_list), 200


# 2. Rute /api/produk/detail (GET: Detail, PUT: Update, DELETE: Hapus)
@app.route("/api/produk/detail", methods=["GET", "PUT", "DELETE"])
def detail_produk():
    produk_id = request.args.get("id")

    if not produk_id:
        return jsonify({"error": "Parameter ID produk wajib disertakan"}), 400

    db = get_db()
    cursor = db.cursor()

    # GET: Detail Produk
    if request.method == "GET":
        cursor.execute("SELECT * FROM produk WHERE id = ?", (produk_id,))
        produk = cursor.fetchone()

        if produk is None:
            return jsonify({"error": "Produk tidak ditemukan"}), 404

        return jsonify(dict(produk)), 200

    # PUT: Update Produk
    elif request.method == "PUT":
        data = request.get_json()
        nama = data.get("nama")
        harga = data.get("harga")
        stok = data.get("stok")

        if not nama or harga is None or stok is None:
            return (
                jsonify({"error": "Data nama, harga, dan stok wajib diisi"}),
                400,
            )

        cursor.execute(
            "UPDATE produk SET nama = ?, harga = ?, stok = ? WHERE id = ?",
            (nama, harga, stok, produk_id),
        )
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Produk tidak ditemukan"}), 404

        return jsonify({"message": "Produk berhasil diperbarui"}), 200

    # DELETE: Hapus Produk
    elif request.method == "DELETE":
        cursor.execute("DELETE FROM produk WHERE id = ?", (produk_id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Produk tidak ditemukan"}), 404

        return jsonify({"message": "Produk berhasil dihapus"}), 200


# 3. Rute /api/transaksi (POST: Buat transaksi baru, GET: Riwayat transaksi)
@app.route("/api/transaksi", methods=["GET", "POST"])
def manage_transaksi():
    db = get_db()

    if request.method == "POST":
        data = request.get_json()
        produk_id = data.get("produk_id")
        jumlah = data.get("jumlah")

        if not produk_id or not jumlah:
            return (
                jsonify({"error": "Data produk_id dan jumlah wajib diisi"}),
                400,
            )

        cursor = db.cursor()
        cursor.execute("SELECT * FROM produk WHERE id = ?", (produk_id,))
        produk = cursor.fetchone()

        if produk is None:
            return jsonify({"error": "Produk tidak ditemukan"}), 404

        if produk["stok"] < jumlah:
            return jsonify({"error": "Stok tidak mencukupi"}), 400

        total_harga = produk["harga"] * jumlah

        # Simpan transaksi
        cursor.execute(
            "INSERT INTO transaksi (produk_id, jumlah, total_harga) VALUES (?, ?, ?)",
            (produk_id, jumlah, total_harga),
        )

        # Kurangi stok produk
        cursor.execute(
            "UPDATE produk SET stok = stok - ? WHERE id = ?",
            (jumlah, produk_id),
        )

        db.commit()

        return (
            jsonify(
                {
                    "message": "Transaksi berhasil",
                    "transaksi_id": cursor.lastrowid,
                    "total_harga": total_harga,
                }
            ),
            201,
        )

    # Method GET
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT t.id, t.produk_id, p.nama AS nama_produk, t.jumlah, t.total_harga, t.tanggal 
        FROM transaksi t
        JOIN produk p ON t.produk_id = p.id
        ORDER BY t.id DESC
    """
    )
    transaksi_list = [dict(row) for row in cursor.fetchall()]
    return jsonify(transaksi_list), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)