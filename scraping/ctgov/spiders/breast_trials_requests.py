import scrapy
import requests
from urllib.parse import urlencode
import time

class BreastTrialsRequestsSpider(scrapy.Spider):
    name = "breast_trials_requests"

    query_cond = "breast cancer"
    page_size = 100
    max_records = 500

    custom_settings = {
        "LOG_LEVEL": "INFO",
        "ROBOTSTXT_OBEY": False,
        "RETRY_ENABLED": False,
        "DOWNLOAD_DELAY": 0,
    }

    def start_requests(self):
        yield scrapy.Request("data:text/plain,start", callback=self.parse, dont_filter=True)

    def parse(self, response):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json,text/plain,*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://clinicaltrials.gov/",
            "Connection": "keep-alive",
        }

        base = "https://clinicaltrials.gov/api/v2/studies"
        token = None
        scraped = 0

        while True:
            params = {"query.cond": self.query_cond, "pageSize": self.page_size, "format": "json"}
            if token:
                params["pageToken"] = token

            url = base + "?" + urlencode(params)
            r = requests.get(url, headers=headers, timeout=30)

            if r.status_code != 200:
                self.logger.error(f"Requests got HTTP {r.status_code} for {url}")
                self.logger.error(f"Body snippet: {r.text[:800].replace(chr(10),' ')}")
                break

            data = r.json()
            studies = data.get("studies", [])
            token = data.get("nextPageToken")

            for st in studies:
                ps = st.get("protocolSection", {}) or {}
                idm = (ps.get("identificationModule", {}) or {})
                sm = (ps.get("statusModule", {}) or {})
                dm = (ps.get("designModule", {}) or {})
                em = (ps.get("eligibilityModule", {}) or {})
                cm = (ps.get("conditionsModule", {}) or {})
                am = (ps.get("armsInterventionsModule", {}) or {})
                sp = st.get("derivedSection", {}) or {}
                misc = sp.get("miscInfoModule", {}) or {}

                conditions = cm.get("conditions") or []
                interventions = am.get("interventions") or []
                intervention_types = [i.get("type") for i in interventions if isinstance(i, dict)]
                countries = misc.get("countries") or []

                yield {
                    "nct_id": idm.get("nctId"),
                    "title": idm.get("briefTitle") or idm.get("officialTitle"),
                    "overall_status": sm.get("overallStatus"),
                    "study_type": dm.get("studyType"),
                    "phases": dm.get("phases"),
                    "start_date": (sm.get("startDateStruct") or {}).get("date"),
                    "completion_date": (sm.get("completionDateStruct") or {}).get("date"),
                    "enrollment": (sm.get("enrollmentInfo") or {}).get("count"),
                    "sex": em.get("sex"),
                    "min_age": em.get("minimumAge"),
                    "max_age": em.get("maximumAge"),
                    "n_conditions": len(conditions),
                    "n_interventions": len(interventions),
                    "intervention_types": "|".join([t for t in intervention_types if t]),
                    "n_countries": len(countries),
                }

                scraped += 1
                if scraped >= self.max_records:
                    self.logger.info(f"Reached max_records={self.max_records}")
                    return

            if not token:
                break

            time.sleep(1.0)  # rate limit

        self.logger.info(f"Finished, scraped={scraped}")
