from linkedin_api import Linkedin
import pandas as pd


relevant_fields = [
    "lastName",
    "headline",
    "firstName",
    "geoLocationName",
    "experience",
    "skills",
    "education"
]


def get_geo_locations(geo_location_name, experience_info):
    location = set(geo_location_name.split(","))
    for experiance in experience_info:
        [location.add(loc) for loc in experiance.get("locationName", "").split(",")]
    return list(location)


def construct_name(first_name, lastname):
    return first_name + " " + lastname


def get_headline(headline):
    return headline


def get_time_period(time_period):
    timeline = ""
    if time_period:
        if time_period.get("endDate"):
            timeline += "{}/{}".format(
                time_period.get("endDate").get("month", ""),
                time_period.get("endDate").get("year", "")
            )
        else:
            timeline = "Present"

        if time_period.get("startDate"):
            timeline += "-{}/{}".format(
                time_period.get("startDate").get("month", ""),
                time_period.get("startDate").get("year", "")
            )
        else:
            timeline += "-Before"
    return timeline


def get_top_3_experience(experiences):
    exp_list = []
    for count, experience in enumerate(experiences):
        if count == 3:
            break
        exp_list.append(
            [
                experience["companyName"],
                experience["title"],
                get_time_period(experience["timePeriod"]),
            ]
        )
    if len(exp_list) == 3:
        return exp_list[0], exp_list[1], exp_list[2]
    elif len(exp_list) == 2:
        return exp_list[0], exp_list[1], ""
    elif len(exp_list) == 1:
        return exp_list[0], "", ""
    return "", "", ""


def get_skills(skills):
    skill_set = set()
    for skill in skills:
        skill_set.add(skill.get("name", ""))
    return list(skill_set)


def extract_batch(educations_info):
    college_name = {"information", "technology", "institute", "indian", "senapati", "manipur", "iiit", "iiitm"}
    for edu_info in educations_info:
        common_words = set(school.lower() for school in edu_info.get("schoolName", "").split(" ")).intersection(college_name)
        if common_words:
            return get_time_period(edu_info.get("timePeriod"))


def extract_relevant_data(data, relevant_fields):
    info_dict = {}
    for field in relevant_fields:
        info_dict[field] = data.get(field, "")

    name = construct_name(info_dict["firstName"], info_dict["lastName"])
    print(name)
    batch = extract_batch(info_dict["education"])
    print(batch)
    headline = get_headline(info_dict["headline"])
    print(headline)
    exp1, exp2, exp3 = get_top_3_experience(info_dict["experience"])
    print(exp1, exp2, exp3)
    skills = get_skills(info_dict["skills"])
    print(skills)
    work_locations = get_geo_locations(info_dict["geoLocationName"], info_dict["experience"])
    print(work_locations)
    return name, batch, headline, exp1, exp2, exp3, skills, work_locations


def is_student(data):
    if data.get("student"):
        return True
    return False


def get_linkedin_profile_data(row):
    print(row[0])
    data = api.get_profile(row[0])
    # data = {'industryName': 'IT Services and IT Consulting', 'lastName': 'Pratap', 'address': 'Jyoti Kunj Colony, Tundla , Firozabad , Uttar Pradesh ,283204', 'locationName': 'India', 'student': False, 'geoCountryName': 'India', 'geoCountryUrn': 'urn:li:fs_geo:102713980', 'geoLocationBackfilled': False, 'elt': True, 'birthDate': {'month': 2, 'day': 8}, 'industryUrn': 'urn:li:fs_industry:96', 'firstName': 'Anit', 'entityUrn': 'urn:li:fs_profile:ACoAACmNJJIBCnbZ3nip6zpdUcYHJydYhECelws', 'geoLocation': {'geoUrn': 'urn:li:fs_geo:105725663'}, 'geoLocationName': 'Tundla, Uttar Pradesh', 'location': {'basicLocation': {'countryCode': 'in'}}, 'headline': 'Software Engineer at Capgemini Engineering || Cloud Services || Automation', 'displayPictureUrl': 'https://media-exp1.licdn.com/dms/image/C5603AQHDK5UKnMaYiA/profile-displayphoto-shrink_', 'profile_id': 'ACoAACmNJJIBCnbZ3nip6zpdUcYHJydYhECelws', 'experience': [{'locationName': 'Gurugram, Haryana, India', 'entityUrn': 'urn:li:fs_position:(ACoAACmNJJIBCnbZ3nip6zpdUcYHJydYhECelws,1840225755)', 'geoLocationName': 'Gurugram, Haryana, India', 'geoUrn': 'urn:li:fs_geo:106442238', 'companyName': 'Capgemini Engineering', 'timePeriod': {'startDate': {'month': 9, 'year': 2021}}, 'company': {'employeeCountRange': {'start': 10001}, 'industries': ['Information Technology and Services']}, 'title': 'Software Engineer', 'region': 'urn:li:fs_region:(in,0)', 'companyUrn': 'urn:li:fs_miniCompany:72092703', 'companyLogoUrl': 'https://media-exp1.licdn.com/dms/image/C4D0BAQGcNoU1nVm4Wg/company-logo_'}], 'skills': [{'name': 'C (Programming Language)', 'standardizedSkillUrn': 'urn:li:fs_miniSkill:438', 'standardizedSkill': {'name': 'C (Programming Language)', 'entityUrn': 'urn:li:fs_miniSkill:438'}}, {'name': 'Python (Programming Language)', 'standardizedSkillUrn': 'urn:li:fs_miniSkill:1346', 'standardizedSkill': {'name': 'Python (Programming Language)', 'entityUrn': 'urn:li:fs_miniSkill:1346'}}, {'name': 'MySQL', 'standardizedSkillUrn': 'urn:li:fs_miniSkill:380', 'standardizedSkill': {'name': 'MySQL', 'entityUrn': 'urn:li:fs_miniSkill:380'}}, {'name': 'PHP', 'standardizedSkillUrn': 'urn:li:fs_miniSkill:261', 'standardizedSkill': {'name': 'PHP', 'entityUrn': 'urn:li:fs_miniSkill:261'}}, {'name': 'Android Studio', 'standardizedSkillUrn': 'urn:li:fs_miniSkill:55003', 'standardizedSkill': {'name': 'Android Studio', 'entityUrn': 'urn:li:fs_miniSkill:55003'}}, {'name': 'HTML5'}, {'name': 'Cascading Style Sheets (CSS)'}, {'name': 'Javascript'}, {'name': 'Jquery'}, {'name': 'Bootstrap'}, {'name': 'Git'}, {'name': 'Jupyter notebook'}, {'name': 'Software Engineering'}, {'name': 'cloud'}], 'education': [{'entityUrn': 'urn:li:fs_education:(ACoAACmNJJIBCnbZ3nip6zpdUcYHJydYhECelws,567914332)', 'school': {'objectUrn': 'urn:li:school:4165000', 'entityUrn': 'urn:li:fs_miniSchool:4165000', 'active': True, 'schoolName': 'Indian Institute of Information Technology Senapati, Manipur', 'trackingId': 'wSRRZ10YSt+qYjGV/FluHA==', 'logoUrl': 'https://media-exp1.licdn.com/dms/image/C560BAQEugDh96mCy9Q/company-logo_'}, 'timePeriod': {'endDate': {'month': 6, 'year': 2021}, 'startDate': {'month': 8, 'year': 2017}}, 'degreeName': 'Bachelor of Technology - BTech', 'schoolName': 'Indian Institute of Information Technology Senapati, Manipur', 'fieldOfStudy': 'Computer Science And Engineering', 'degreeUrn': 'urn:li:fs_degree:250', 'schoolUrn': 'urn:li:fs_miniSchool:4165000'}, {'entityUrn': 'urn:li:fs_education:(ACoAACmNJJIBCnbZ3nip6zpdUcYHJydYhECelws,737512427)', 'grade': '85.2%', 'timePeriod': {'endDate': {'month': 5, 'year': 2016}, 'startDate': {'month': 7, 'year': 2014}}, 'degreeName': 'Higher Secondary', 'schoolName': 'O. D. V. INTER COLLEGE TUNDLA FIROZABAD'}, {'entityUrn': 'urn:li:fs_education:(ACoAACmNJJIBCnbZ3nip6zpdUcYHJydYhECelws,737513198)', 'grade': '85.3%', 'timePeriod': {'endDate': {'month': 5, 'year': 2014}, 'startDate': {'month': 7, 'year': 2013}}, 'degreeName': 'Senior Secondary', 'schoolName': 'TUNDLA PUBLIC H S S TUNDLA FIROZABAD'}]}
    print(data)

    if is_student(data):
        pass
    else:
        return pd.Series(extract_relevant_data(data, relevant_fields))


if __name__ == '__main__':
    df = pd.read_csv("linkedin_username.csv")
    api = Linkedin('aman.ranjanverma@gmail.com', '***password**')
    df_out = df.apply(get_linkedin_profile_data, axis=1)
    df_out.columns = ["Name", "Batch", "Headline", "Experiance_1", "Experiance_2", "Experiance_3", "Skills", "Locations"]
    df_out.to_csv("linkedin_profile_details.csv", index=False)
