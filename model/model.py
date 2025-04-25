from database.DAO import DAO
from model.retailer import Retailer


class Model:
    def __init__(self):
        self._DAO = DAO()

    def set_filtri(self, chiave_dropdown1, chiave_dropdown2, chiave_dropdown3):
        result = self._DAO.get_filtri(chiave_dropdown1, chiave_dropdown2, chiave_dropdown3)
        return result

    def getAnalisi(self,chiave_dropdown1, chiave_dropdown2, chiave_dropdown3):
        result = self._DAO.getAnalisi(chiave_dropdown1, chiave_dropdown2, chiave_dropdown3)
        return result
