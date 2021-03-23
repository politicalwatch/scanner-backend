import csv

class LinesOfAction():
    targets_denylist = [
        '2.3',
        '3.8',
        '4.7',
        '5.5',
        '15.1',
        '16.1',
        '16.3',
        '16.6'
    ]

    def extract(results):
        extractor = LinesOfAction()
        return extractor.get(results)

    def get(self, results):
        kb_lines = self.get_kb_lines()
        lines_by_tag = dict()
        with open('./data/lines.csv') as csvfile:
            csvreader = csv.reader(csvfile)
            for d in csvreader:
                lines_by_tag[d[1]] = d[0]

        result = results['result']
        tags = result['tags']
        courses_of_action = []
        if len(tags) != 0:
            for tag in tags:
                subtopic = self.extract_subtopic_number(tag['subtopic'])
                if not self.is_target_in_denylist_for_lines(subtopic):
                    try:
                        tag['course_of_action'] = kb_lines[subtopic]
                        courses_of_action.append(kb_lines[subtopic])
                    except KeyError:
                        pass
                else:
                    try:
                        tag['course_of_action'] = lines_by_tag[tag['tag']]
                        courses_of_action.append(lines_by_tag[tag['tag']])
                    except KeyError:
                        pass
        result['courses_of_action'] = list(set(courses_of_action))

    def extract_subtopic_number(self, subtopic):
        splitted = subtopic.split(' ', 1)
        return splitted[0]

    def get_kb_lines(self):
        kb = dict()
        with open('./data/matrix.csv') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if row[0] not in self.targets_denylist:
                    kb[row[0]] = row[1]
        return kb

    def is_target_in_denylist_for_lines(self, target):
        return target in self.targets_denylist


