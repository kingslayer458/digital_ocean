import os
from pydo import Client
import json
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DIGITAL_OCEAN_TOKEN")

if not TOKEN:
    raise ValueError("DIGITAL_OCEAN_TOKEN not found")

def digital_ocean_vm_extractor(TOKEN):
    try:
        client = Client(token=TOKEN)
        account = client.account.get()
        print("Email  :", account["account"]["email"])
        print("Status :", account["account"]["status"])
        resp = client.droplets.list()
    except Exception as e :
        print(f"failed to connect digital ocean api :{e}")
        raise

    return resp

def vm_details_extractor(resp):
    king = []

    for droplet in resp["droplets"]:

        vm_id = droplet["id"]
        name = droplet["name"]
        memory = droplet["memory"]
        vcpus = droplet["vcpus"]
        disk =  droplet["disk_info"][0]["size"]["amount"]
        disk_unit =  droplet["disk_info"][0]["size"]["unit"]
        status = droplet["status"]
        created_at = droplet["created_at"]
        image= droplet["image"]["name"]
        public_ip= droplet["networks"]["v4"][0]["ip_address"]
        private_ip= droplet["networks"]["v4"][1]["ip_address"]
        size_slug = droplet["size_slug"]
        region = droplet["region"]["name"]

        summary = {
            "vm_id": vm_id,
            "name": name,
            "memory": memory,
            "vcpus": vcpus,
            "disk_size": f"{disk} {disk_unit}",
            "status": status,
            "created_at": created_at,
            "image": image,
            "public_ip": public_ip,
            "private_ip": private_ip,
            "size_slug":size_slug,
            "region":region
        }

        king.append(summary)

    return king

def main():
    try:
        resp = digital_ocean_vm_extractor(TOKEN)
        data = vm_details_extractor(resp)
        print(json.dumps(data, indent=4))
        with open ("vm_data_digital_ocean.json","w") as f:
            json.dump(data,f,indent=4)
            
    except Exception as e:
        print(f"vm extraction failed : {e}")
        raise


if __name__ == "__main__":
     main()
