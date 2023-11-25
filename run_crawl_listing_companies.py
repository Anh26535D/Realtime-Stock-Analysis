from crawler.VietStock import ListingCompanyVietStock

crawler = ListingCompanyVietStock()
data = crawler.run()
data.to_csv('data/list_companies.csv', index=False)