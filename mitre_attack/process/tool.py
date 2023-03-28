from stix2 import Filter
from package import get_data, datacomponents_detecting_technique


if __name__ == '__main__':
    techniques: list = get_data(Filter("type", "=", "attack-pattern"))
    techniques_map_datacomponent_dict: dict = datacomponents_detecting_technique()

    search_id: str = 'T1546.016'  # 根据 id 查询单条 mitre att&ck

    for technique in techniques:
        if technique["external_references"][0]["external_id"] == search_id:
            print("name: \n" + technique["name"] + "\n")

            if 'description' in technique:
                print("description: \n" + technique["description"] + "\n")

            print("detects: ")
            if 'x_mitre_data_sources' in technique:
                detect_list: list = techniques_map_datacomponent_dict[technique["id"]]
                for item in detect_list:
                    print(item['relationship']['description'])

