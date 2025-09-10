from dataclasses import dataclass
from typing import Optional


@dataclass
class JobRecord:
    site: str
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    job_url: Optional[str] = None
    work_type: Optional[str] = None
    scraped_at: Optional[str] = None

    def as_dict(self):
        return {
            "site": self.site,
            "job_title": self.job_title,
            "company_name": self.company_name,
            "location": self.location,
            "job_url": self.job_url,
            "work_type": self.work_type,
            "scraped_at": self.scraped_at,
        }
