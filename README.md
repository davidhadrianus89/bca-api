# bca-api

How To Make It Works (For Developer Only)

OS version ubuntu (should not problem with version 16 +) make sure you have installed python 2.7

1. git clone https://github.com/davidhadrianus89/bca-api.git
2. cd bca-api
3. pip install -r requirement.txt
4. python api.py
5. Open In browser localhost:5000/api-bca

    If you see something like this
    
    "Hello, Congratulation!! You can access my trial BCA API :)" .
    
    Then you can move forward to test the real api.

Open Your Postman, Swagger or other tools to test Restful API


1. localhost:5000/api-bca/saldo
    Method : Post
    params :
        {
            "username" : "your username",
            "username" : "your password"
        }
    
    response:
    {
    "Info rekening anda": {
        "No Rekening": "",
        "Sisa Saldo": ""
    }
}
    
    
2. localhost:5000/api-bca/api-bca/transaksi

    Method : Post
    params :
        {
            "username" : "your username",
            "username" : "your password"
        }
    
    response:
    
    {
    "Info rekening anda": {
        "Informasi Saldo": {
            "Mata Uang": "",
            "Nama": "",
            "No. Rek": "",
            "Periode": ""
        },
        "Ringkasan Mutasi": {
            "Mutasi Debet": "",
            "Mutasi Kredit": "",
            "Saldo Akhir": "",
            "Saldo Awal": ""
        },
        "Transaksi Mutasi Rekening": [
            {
                "KETERANGAN": "",
                "TGL.": ""
            },
            {
                "KETERANGAN": "",
                "TGL.": ""
            },
            {
                "KETERANGAN": "",
                "TGL.": ""
            },
            {
                "KETERANGAN": "",
                "TGL.": ""
            }
        ]
    }
}
