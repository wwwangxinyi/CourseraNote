
punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
# lists of words to use
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())

negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())


def strip_punctuation(str):
    for char in punctuation_chars:
        str = str.replace(char, "")
    return str


def get_pos(str):
    words = strip_punctuation(str)
    words = words.lower().split()
    count = 0
    for word in words:
        if word in positive_words:
            count = count + 1
    return count


def get_neg(str):
    words = strip_punctuation(str)
    words = words.lower().split()
    count = 0
    for word in words:
        if word in negative_words:
            count = count + 1
    return count


twi_content = []
with open('project_twitter_data.csv', 'r', encoding='UTF-8') as twi:
    twi.readline()
    twi_content = twi.readlines()

with open('resulting_data.csv', 'w') as csvfile:
    header = "{}, {}, {}, {}, {}".format("Number of Retweets", "Number of Replies", "Positive Score", "Negative Score",
                                         "Net Score")
    csvfile.write(header)
    csvfile.write('\n')

    temp = []
    for line in twi_content:
        ans = []
        temp = line.split(',')

        # Number of Retweets
        ans.append(temp[1])

        # Number of Replies
        ans.append(int(temp[2]))

        twi_content = strip_punctuation(temp[0])
        # Positive Score
        pos_s = get_pos(twi_content)
        ans.append(pos_s)

        # Negative Score
        neg_s = get_neg(twi_content)
        ans.append(neg_s)

        csv_line = "{},{},{},{},{}\n".format(
            ans[0], ans[1], ans[2], ans[3], ans[2] - ans[3])
        csvfile.write(csv_line)
