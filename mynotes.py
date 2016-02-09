""" Delete here when submitting!!!
#############################################################################
Notes which demonstrate an understanding of:
	- Servers: 
		how servers handle requests, process them, and deliver responses
	- The Importance of Validating Input: 
		acknowledge the importance of validating user input, expecially the implications that validation has on site security and user experience.
	- HTML Templates and Abstraction:
		an understanding of why programmers use HTML templates, how these templates allow programmers to avoid repetition, and understanding of WHY avoiding repetition is important
#############################################################################
"""


unit1 = {
	"unit_title": "How Servers Work",
	"concepts": {
		"concept1": {
			"concept_title": "Client and Server",
			"concept_description": "Your computer(= Client) is connected to a server through a network called the Internet. When your browser requests a page, the server sends back the requested page.",
			"image": "http://i.imgur.com/0vPATU6.png" 
		},
		"concept2": {
			"concept_title": "URL",
			"concept_description": "URL is abbreviation of Uniform Resource Locator.",
			"image": "http://i.imgur.com/vdwt3eC.png"
		},
		"concept3": {
			"concept_title": "GET vs POST",
			"concept_description": "Requests which are sent from your browser to a server. A type of requests making to the server is called 'method': GET(= get a document from the server) & POST(send data to the server). When making requests, request line if followed by a number of headers.",
			"image": "http://i.imgur.com/uot62jp.png"
		},
		"concept4": {
			"concept_title": "Purpose of a Server",
			"concept_description": {
				"description": "Servers respond to HTTP requests from a browser:",
				"html_list": [
					"Static requests --- pre-written files, images",
					"Dynamic requests --- made on the fly by Web application on a web server, which generates content that the browser requests, such as Facebook or Google Search Engine"
				]
			}
		}
	}
}

unit2 = {
	"unit_title": "Validating Inputs is Important!!",
	"concepts": {
		"concept1": {
			"concept_title": "Why input validation is important?",
			"concept_description": "When a user enters bad input, varidating input will prevent our web application from being hacked. Make sure to validate data on the server side as it's more sequre than one on the Client side. If you are using Python and HTML template for making a web app, validation should occur in a python file. If you get an error, redirect to the form without storing invalid data to a database.",
		},
		"concept2": {
			"concept_title": "Steps for Validation & Redirection",
			"concept_description": {
				"description" : "With varidation, the user will know that there's an error.",
				"html_list": [
					"Verify the user's input",
					"On error, render form again",
					"Include error message",
					"With a valid input, store data and redirect a page without an error message"
				]
			},
			"image": "http://i.imgur.com/NibKQte.png"
		},
		"concept3": {
			"concept_title": "HTML Escaping",
			"concept_description": "If a user enters HTML into the input, it will mess up the web form. It's important to escape the HTML characters. ",
				"image": "http://i.imgur.com/g4y4GV1.png?1"
		}		
	}
}

unit3 = {
	"unit_title": "HTML Templates & Abstraction",
	"concepts": {
		"concept1": {
			"concept_title": "String substitution",
			"concept_description": {
				"description": "One way to format html is to use the modulus operator %s in html string in Python. But it has quite a few problems;",
				"html_list": [
					"Hardcoded %s everywhere and difficult to change",
					"Putting html in python code as strings won't get syntax highlighted",
					"Can be made more clear",
					"If you miss changing %s, output will show %s as it is"
				]
			} 
		},
		"concept2": {
			"concept_title": "HTML Templates",
			"concept_description": {
				"description": "Better way than string substitution is to use Templates. In this lesson, we use jinja2 templates. With templates, you can...",
				"html_list": [
					"Separate different types of code (ex. sparate HTML from Python)",
					"Have better organized and more readable code",
					"More secure websites with autoescaping feature",
					"HTML that is easier to manipulate"
				]
			}
		},
		"concept3": {
			"concept_title": "Template Inheritance",
			"concept_description": "The most advantage of using jinja2 template is template inheritance, which 'allow us to build a base 'skeleton' template that contains all the common elements of your site and defines blocks that child template can override'. (http://jinja.pocoo.org/docs/dev/templates/#template-inheritance) So, the template inheritance can avoid writing the same code over and over again when generating html. "
		}
	}
}

unit4 = {
	"unit_title": "Databases",
	"concepts": {
		"concept1": {
			"concept_title": "What is a Database?",
			"concept_description": "A program that stores and retrieves large amount of structured data. It also refers to the machine running that program and a system of machines running the program together to store/retrieve data."
		},
		"concept2": {
			"concept_title": "Benefits of Databases",
			"concept_description": "Databases can take huge amount of data and answer queries on them in a reasonable amount of time without having to write a lot of custom code."
		},
			"concept2": {
		"concept_title": "Benefits of Databases",
		"concept_description": "Databases can take huge amount of data and answer queries on them in a reasonable amount of time without having to write a lot of custom code."
		}
	}
}

all_notes = [unit1, unit2, unit3, unit4]

concepts_order = ["concept1", "concept2", "concept3", "concept4"]

