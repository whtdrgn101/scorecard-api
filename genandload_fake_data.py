import click
from faker import Faker
import routes.schemas as schemas
from datetime import datetime
import json
import requests
import random 

@click.command()
@click.option('--user_count', default=10, required=False, type=int, show_default=True, help='Number of test users to generate.')
@click.option('--bow_count', default=5, required=False, type=int, show_default=True, help='Number of bows to create per user.')
@click.option('--round_count', default=5, required=False, type=int, show_default=True, help='Number of rounds to create per bow.')
@click.option('--end_count', default=10, required=False, type=int, show_default=True, help='Number of ends to create per round.')
def main(user_count: int = 10, bow_count:int = 5, round_count:int = 5, end_count:int = 10):
    fake = Faker()
    headers = {"Content-type":"application/json"}
    base_url = "http://localhost:8000"
    user_url = f"{base_url}/user"

    for usr in range(1, user_count):
        user = schemas.UserCreate(name = fake.name(), email = fake.email())
        json_data = json.dumps(user, cls=schemas.CreationEncoder)
        response = requests.post(user_url, data = json_data, headers=headers)
        if response.status_code == 200:
            print(f"Create user: {user.name}")
            new_user = json.loads(response.text)
            new_bow_ids = []

            for b in range(1,bow_count):
                bow = schemas.BowCreate(name=f"{user.name}'s Test Bow #{b}", user_id=new_user['id'], bow_type_id=b, draw_weight=float(random.randint(25,75)))
                json_data = json.dumps(bow, cls=schemas.CreationEncoder)
                response = requests.post(f"{user_url}/{new_user['id']}/bow", data=json_data, headers=headers)
                if response.status_code == 200:
                    new_bow = json.loads(response.text)
                    new_bow_ids.append(new_bow['id'])
                else:
                    raise Exception("Failed to create bow")
                
            print(f"Generated Bows for user: {user.name}")
            for bow_id in new_bow_ids:
                for r in range(1,round_count):
                    round = schemas.RoundCreate(round_date=datetime.now(), bow_id=bow_id, user_id=new_user['id'], round_type_id=r)
                    json_data = json.dumps(round, cls=schemas.CreationEncoder)
                    response = requests.post(f"{user_url}/{new_user['id']}/round", data=json_data, headers=headers)
                    if response.status_code == 200:
                        new_round = json.loads(response.text)
                        for i in range(1,end_count):
                            end = schemas.EndCreate(round_id = new_round['id'], score=random.randint(1, 30))
                            json_data = json.dumps(end, cls=schemas.CreationEncoder)
                            response = requests.post(f"{user_url}/{new_user['id']}/round/{new_round['id']}/end", data=json_data, headers=headers)
                    else:
                        raise Exception(f"Failed to create round for bow: {bow_id}")
                    
            print(f"Generated Rounds for user: {user.name}")
        else:
            print(f"Error: {response.status_code}")
            raise Exception("Coult not create user")

if __name__ == "__main__":
    main()