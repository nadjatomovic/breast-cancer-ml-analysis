import scrapy
from urllib.parse import urlencode

class BreastTrialsSpider(scrapy.Spider):
    name = "breast_trials"
    allowed_domains = ["clinicaltrials.gov"]

    query_cond = "breast cancer"
    page_size = 100
    max_records = 400

    # NATERAJ Scrapy da prosledi 403 u parse
    handle_httpstatus_list = [403]

    custom_settings = {
        "DOWNLOAD_DELAY": 1.3,
        "AUTOTHROTTLE_ENABLED": True,
        "LOG_LEVEL": "INFO",
        "ROBOTSTXT_OBEY": False,

        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json,text/plain,*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://clinicaltrials.gov/",
            "Connection": "keep-alive",
        },

        # Debug: nemoj da Retry skriva problem
        "RETRY_ENABLED": False,
    }

    def start_requests(self):
        params = {
            "query.cond": self.query_cond,
            "pageSize": self.page_size,
            "countTotal": "true",
            "format": "json",
        }
        url = "https://clinicaltrials.gov/api/v2/studies?" + urlencode(params)

        yield scrapy.Request(
            url,
            callback=self.parse,
            errback=self.errback_log,
            dont_filter=True,
            meta={"handle_httpstatus_all": True},  # dodatno forsiranje
        )

    def errback_log(self, failure):
        self.logger.error("Request failed (errback).")
        self.logger.error(repr(failure))

        # Ako postoji response, ispiši info
        response = getattr(failure.value, "response", None)
        if response is not None:
            self.logger.error(f"Errback got HTTP {response.status} for {response.url}")
            self.logger.error(f"Body snippet: {response.text[:600].replace(chr(10),' ')}")

    def parse(self, response):
        self.logger.info(f"Got HTTP {response.status} for {response.url}")

        # Ako je 403, ispiši telo da znamo šta blokira
        if response.status == 403:
            snippet = response.text[:800].replace("\n", " ")
            self.logger.error(f"403 body snippet: {snippet}")
            return

        data = response.json()
        studies = data.get("studies", [])
        next_page_token = data.get("nextPageToken")

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
                "n_conditions": len(cm.get("conditions") or []),
                "n_interventions": len(am.get("interventions") or []),
            }

        scraped_so_far = self.crawler.stats.get_value("item_scraped_count", 0) or 0
        if scraped_so_far >= self.max_records:
            self.logger.info(f"Reached max_records={self.max_records}, stopping.")
            return

        if next_page_token:
            params = {
                "query.cond": self.query_cond,
                "pageSize": self.page_size,
                "pageToken": next_page_token,
                "format": "json",
            }
            next_url = "https://clinicaltrials.gov/api/v2/studies?" + urlencode(params)

            yield scrapy.Request(
                next_url,
                callback=self.parse,
                errback=self.errback_log,
                dont_filter=True,
                meta={"handle_httpstatus_all": True},
            )
