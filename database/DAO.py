from database.DB_connect import DBConnect
from model.retailer import Retailer

class DAO():
    @staticmethod
    def get_retailer() -> list[Retailer] | None:
        """
            Funzione che legge tutti i retailler nel database
            :return: una lista con tutti i corsi presenti
            """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is not None:
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT * FROM go_retailers")
            for row in cursor:
                result.append(Retailer(row["Retailer_code"], row["Retailer_name"], row["Type"], row["Country"]))
            cursor.close()
            cnx.close()
            return result
        else:
            print("Could not connect")
            return None
    @staticmethod
    def get_brands():
        """
        Funzione che legge tutti i brand nel database
        :return: un set con tutti i brand (stringhe uniche)
        """
        cnx = DBConnect.get_connection()
        result = set()  # inizializza un set vuoto, non un dizionario
        if cnx is not None:
            cursor = cnx.cursor()
            cursor.execute("SELECT Product_brand FROM go_sales.go_products")
            for row in cursor:
                result.add(row[0])  # aggiunge ogni brand al set
            cursor.close()
            cnx.close()
            return result
        else:
            print("Could not connect")
            return None
    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is not None:
            cursor = cnx.cursor()
            cursor.execute("SELECT DISTINCT YEAR(Date) AS anno FROM go_sales.go_daily_sales ORDER BY anno;")
            for row in cursor:
                result.append(row[0])  # oppure row["anno"] se usi dictionary=True
            cursor.close()
            cnx.close()
            return result
        else:
            print("Could not connect")
            return []

    @staticmethod
    def get_filtri(chiave_dropdown1, chiave_dropdown2, chiave_dropdown3):
            cnx = DBConnect.get_connection()
            result = []
            if cnx is not None:
                cursor = cnx.cursor()
                query = """
                SELECT gds.Date, (Unit_sale_price * Quantity) AS Ricavo, gds.Retailer_code, gds.Product_number
                FROM go_sales.go_daily_sales AS gds
                JOIN go_sales.go_products AS gp ON gds.Product_number = gp.Product_number
                WHERE gp.Product_brand = COALESCE(NULLIF(%s, 'nessun filtro'), gp.Product_brand)
                AND gds.Retailer_code = COALESCE(NULLIF(%s, 'nessun filtro'), gds.Retailer_code)
                AND YEAR(gds.Date) = COALESCE(NULLIF(%s, 'nessun filtro'), YEAR(gds.Date))
                ORDER BY Ricavo DESC
                LIMIT 5;
                """

                cursor.execute(query, (chiave_dropdown2, chiave_dropdown3, str(chiave_dropdown1)))
                for row in cursor:
                    result.append(row)  # oppure row["anno"] se usi dictionary=True
                cursor.close()
                cnx.close()
                return result
            else:
                print("Could not connect")
                return []


    @staticmethod
    def getAnalisi(chiave_dropdown1, chiave_dropdown2, chiave_dropdown3):
            cnx = DBConnect.get_connection()
            result = []
            if cnx is not None:
                cursor = cnx.cursor()
                query = """SELECT 
                            IFNULL(SUM(Unit_sale_price * Quantity), 0) AS Ricavo,
                            IFNULL(COUNT(Date), 0) AS NumeroVendite,
                            IFNULL(COUNT(DISTINCT Retailer_code), 0) AS NegoziCoinvolti,
                            IFNULL(COUNT(DISTINCT gds.Product_number), 0) AS ProdottiCoinvolti
                        FROM go_sales.go_daily_sales AS gds
                        JOIN go_sales.go_products AS gp 
                            ON gds.Product_number = gp.Product_number
                        WHERE gp.Product_brand = COALESCE(NULLIF(%s, 'nessun filtro'), gp.Product_brand)
                        AND gds.Retailer_code = COALESCE(NULLIF(%s, 'nessun filtro'), gds.Retailer_code)
                        AND YEAR(gds.Date) = COALESCE(NULLIF(%s, 'nessun filtro'), YEAR(gds.Date))"""


                cursor.execute(query, (chiave_dropdown2, chiave_dropdown3, str(chiave_dropdown1)))
                for row in cursor:
                    result.append(row)  # oppure row["anno"] se usi dictionary=True
                cursor.close()
                cnx.close()
                return result
            else:
                print("Could not connect")
                return []

