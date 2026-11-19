
from tools.supplier_tools import find_alternative_suppliers
from tools.inventory_tools import check_inventory
from tools.logistics_tools import compare_transport_options

print("\n===== SUPPLIER ANALYSIS =====")
print(find_alternative_suppliers("Electronics", 500))

print("\n===== INVENTORY ANALYSIS =====")
print(check_inventory("Electronics", 500))

print("\n===== LOGISTICS ANALYSIS =====")
print(compare_transport_options(5))
