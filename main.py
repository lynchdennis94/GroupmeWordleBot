import json
import groupme #TODO: Eventually replace with a dedicated library

# File paths (relative to main script)
# For Test Group
config_file_path = "files/testconfig.json"
stats_file_path = "files/teststats.json"
# For Real Group
# config_file_path = "files/config.json"
# stats_file_path = "files/stats.json"

# Config file keys
config_access_token_key = "access_token"
config_bot_id_key = "bot_id"
config_group_id_key = "group_id"
config_since_id_key = "since_id"
config_message_limit_key = "message_limit"
config_time_between_checks_key = "time_between_checks"
config_next_scoring_time_key = "next_scoring_time"

# Stats file keys
stats_last_read_message_id_key = "last"

if __name__ == "__main__":
    while True:
        config_file = open(config_file_path, 'r+')

        config_data = json.load(config_file)
        access_token = config_data[config_access_token_key]
        bot_id = config_data[config_bot_id_key]
        group_id = config_data[config_group_id_key]
        since_id = config_data[config_since_id_key]
        message_limit = config_data[config_message_limit_key]

        # Get the messages since last time
        curl_response = groupme.get_messages(access_token, group_id, since_id=since_id, limit=message_limit)

        if curl_response != "":
            messages = json.loads(curl_response)["response"]["messages"]

            # For each message, parse through for the wordle mark
            last_message_read = None
            for message in messages:
                # If the wordle message is found, extract the relevant data from it
                message_text = message["text"]
                message_id = message["id"]
                message_author = message["name"]
                if last_message_read is None:
                    last_message_read = int(message_id)
                print(message_id)
                print(message_author)
                print(message_text)

            # Update the scoring information for any players

            # Save information to the log file
            config_data[config_since_id_key] = last_message_read

        config_file.seek(0)
        config_file.write(json.dumps(config_data))
        config_file.close()

        # Determine if a message should be sent

        break
