
reservation_dict = {}


def user_and_day_insert(user_id: str, day: str) -> dict:
    reservation_dict[f"{user_id}"] = [day]
    return reservation_dict


def day_and_time_list_insert(user_id: str, time: str) -> dict:
    reservation_dict[f"{user_id}"].append(time)
    return reservation_dict


def get_reservation_data(user_id: int) -> list:
    res_list = reservation_dict[f"{user_id}"]
    return res_list


def reset_data():
    global reservation_dict
    reservation_dict = {}

