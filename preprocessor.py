import re
import pandas as pd



def preprocess(data):

    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, "message_date": dates})

    df.rename(columns={"message_date": "Date"}, inplace=True)

    # separating the users and messages
    names = []
    messagess = []
    for message in df["user_message"]:
        entry = re.split("([\w\W]+?)-\s", message)
        entry[1:]  # username
        names.append(entry[1])
        messagess.append(entry[2])

    df["Time_format"] = names
    df["message"] = messagess
    df.drop(columns=["user_message"], inplace=True)
    df.head()

    # separating the users and messages
    users = []
    message = []
    for messages in df["message"]:
        entry = re.split("([\w\W]+?):\s", messages)
        if entry[1:]:  # username
            users.append(entry[1])
            message.append(entry[2])
        else:
            users.append("group_notification")
            message.append(entry[0])

    df["Name"] = users
    df["Message"] = message
    df.drop(columns=["message"], inplace=True)
    df.head()

    df['Date'] = pd.to_datetime(df['Date'])

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month_name()
    df["Month_num"] = df["Date"].dt.month
    df["date"] = df["Date"].dt.date
    df["Day"] = df["Date"].dt.day
    df["Day_name"] = df["Date"].dt.day_name()
    df["Hour"] = df["Date"].dt.hour
    df["Minute"] = df["Date"].dt.minute

    Period = []
    for Hour in df[["Day_name", "Hour"]]["Hour"]:
        if Hour == 11:
            Period.append(str(Hour) + "-" + str("12"))
        elif Hour == 1:
            Period.append(str("12") + "-" + str(Hour + 1))
        else:
            Period.append(str(Hour) + "-" + str(Hour + 1))

    df["Period"] = Period
    df["period"] = df['Period'].astype(str) + " " + df["Time_format"]

    return df




