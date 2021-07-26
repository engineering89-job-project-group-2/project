import requests
import lxml.html as lh
import os
import pandas as pd


class RolesScrap:
    def scrap(self, role):
        request = requests.get("https://www.itjobswatch.co.uk/jobs/uk/{}.do".format(role.lower()))
        doc = lh.document_fromstring(request.content)

        roles = doc.find_class('summary')  # getting all job data entries from site

        specific = roles[0]  # specific for this job
        general = roles[1]  # general for this area of job

        spec_list = []
        for i in range(len(specific)):
            spec = str(specific[i].text_content())
            spec = os.linesep.join([s for s in spec.splitlines() if s.strip()])
            # print(spec)
            # removing blank lines
            spec = spec.split("\n")  # separator from scraped table entries
            spec_list.append(spec)

        spec_list.remove(spec_list[0])
        spec_list.remove(spec_list[0])

        # print(spec_list)
        tot_spec_list = []

        for item in spec_list:
            for s in item:
                s = s[2:]
                tot_spec_list.append(s)

        def chunk_it(seq, num):
            avg = len(seq) / float(num)
            out = []
            last = 0.0

            while last < len(seq):
                out.append(seq[int(last):int(last + avg)])
                last += avg

            return out

        new_spec_list = chunk_it(tot_spec_list, 14)
        # # print(new_spec_list)
        spec_db = pd.DataFrame(new_spec_list,
                               columns=["Category", "6 Months to Now", "Same Period 2020", "Same Period 2019"])
        # print(spec_db)

        gen_list = []
        for i in range(len(general)):
            gen = str(general[i].text_content())
            gen = os.linesep.join([s for s in gen.splitlines() if s.strip()])
            # print(spec)
            # removing blank lines
            gen = gen.split("\n")  # separator from scraped table entries
            gen_list.append(gen)
        # print(gen_list)
        gen_list.remove(gen_list[0])

        # print(gen_list)
        tot_gen_list = []

        for item in gen_list:
            for s in item:
                s = s[2:]
                tot_gen_list.append(s)

        new_gen_list = chunk_it(tot_gen_list, 11)

        # gen_db = pd.DataFrame(new_gen_list, columns=["Category", "6 Months to Now", "Same Period 2020", "Same Period 2019"])
        # pd.set_option("display.max_rows", None, "display.max_columns", None)

        # print(gen_db)
        return new_gen_list

