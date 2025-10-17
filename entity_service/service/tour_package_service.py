# entity_service/service/tour_package_service.py
import requests # Untuk memanggil destination service jika terpisah, atau langsung query DB jika satu layanan

class TourPackageService:
    # ... __init__ dan method lainnya ...

    def get_tour_with_destination(self, tour_id):
        # 1. Ambil data tour package
        tour_data = self._get_tour_from_db(tour_id) 
        if not tour_data:
            return None

        # 2. Ambil data destination berdasarkan destination_id
        destination_data = self._get_destination_from_db(tour_data['destination_id'])
        
        # 3. Gabungkan datanya
        tour_model = TourPackageModel(**tour_data)
        tour_dict = tour_model.to_dict()
        
        if destination_data:
            destination_model = DestinationModel(**destination_data)
            tour_dict['destination'] = destination_model.to_dict() # Tambahkan objek destination
        else:
            tour_dict['destination'] = None

        return tour_dict