from generation.gen_person import PersonProfile

person = PersonProfile()
person.generate_person_profile()
df = person.create_dataframe()

print(df)
