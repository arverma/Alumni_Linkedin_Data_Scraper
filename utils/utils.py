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


def construct_name(first_name, lastname, user_id):
    return '=HYPERLINK("https://www.linkedin.com/in/{}", "{}")'.format(user_id, first_name + " " + lastname)


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


def extract_relevant_data(data, relevant_fields, user_id):
    info_dict = {}
    for field in relevant_fields:
        info_dict[field] = data.get(field, "")

    name = construct_name(info_dict["firstName"], info_dict["lastName"], user_id)
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