#!/usr/bin/env python
import web
import requests
import json

urls = (
	'/sumnaturals', 'sum_naturals',
)

app = web.application(urls, globals())

class sum_naturals:
	def POST(self):
		data = web.data()
		number = int(data.split('=')[1])
		res = 0
		for i in range(1, number + 1):
			res += i;
		return res


if __name__ == "__main__":
    app.run()
