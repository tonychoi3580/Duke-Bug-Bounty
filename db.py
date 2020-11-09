import psycopg2

con = psycopg2.connect(
    host = "127.0.0.1"
    database = "bugbounty"
    user = "tonychoi"
    password = "bg358016"
)

cur = con.cursor()

cur.execute("select netid, name from users")

rows = cur.fetchall()
for r in rows:
    print("netid {r[0]} name {r[1]}")


con.close()