from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

email1 = """Dear Jayden Udall -

We want to confirm that your application for the JR1986530 NVIDIA 2025 Internships: Hardware Engineering role has been received.

We are always looking for amazing people to join us in doing their life’s work at NVIDIA, and we’re grateful that you took the time to apply for this opportunity.

We will review your application against the open position, and contact you to arrange an interview if the role is a good match for your qualifications.

Thanks again for your interest in NVIDIA.

Best Regards,

The NVIDIA Recruiting Team"""

email2 = """Dear Jayden Udall -

We want to confirm that your application for the JR1987620 NVIDIA 2025 Ignite Internships: Software Engineering role has been received.

We are always looking for amazing people to join us in doing their life’s work at NVIDIA, and we’re grateful that you took the time to apply for this opportunity.

We will review your application against the open position, and contact you to arrange an interview if the role is a good match for your qualifications.

Thanks again for your interest in NVIDIA.

Best Regards,

The NVIDIA Recruiting Team
"""
email3 = """Greetings,
Thank you for setting up a new profile on Southwest Research Institute's Resumé/Application (ResApp).
 You can log back into your account any time using your user name jaydenudall to see the status of any positions you applied to, 
 update your information, or search for new job openings!
"""
email4 = """Hi Jayden!

Thank you so much for your interest in Truveta and taking the time to apply to our Undergrad Software Engineering Intern - Service Quality. We just wanted to let you know that we received your application, and that we're looking forward to reviewing it.

If your application seems like a good fit for the position we will contact you soon.

Have a great day!

Regards,
Your Truveta hiring team
"""
email5 = """Hello Jayden, 
 
Thank you for your interest in joining the Keysight Technologies Team!
 
We have received your application for the position of Software Development Engineering Internship – Recruiting at WE24 (2024-44269). We will review your application and keep you posted if you are shortlisted for an interview, otherwise your resume/CV will be kept for future consideration.
 
Sincerely,
 
Keysight Talent Acquisition Team
 
P.S. Feel free to sign up for email updates of new jobs at Keysight you might be interested in...now or in the near future.  You can set up email alerts by performing a search on the career portal listings page.  You will then be prompted to save an email alert.  """
email6 = """Jayden,

Congratulations on taking the first step for a chance to be a part of Okta! We are thrilled and humbled that you are interested in being part of Okta’s momentum. Kindly be advised that due to an exceptionally high number of applications, there might be a delay in our response to you. Thanks in advance for your patience! If you are selected to move forward in the process, we’ll be in touch.

In the meantime, we invite you to learn more about Okta and what we do:

We’ve attached our core values and how they impact the way we work. Please take a moment to read through them.
If you’re interested in learning about what it’s like to work for Okta, check out the #lifeatOkta series, and take a peek at our other channels, like LinkedIn, Twitter, Facebook, YouTube, and our blog.
Here at Okta, we care about supporting nonprofits and the greater community. We encourage you to learn more about Okta for Good, our social impact initiative.
Stay informed on the latest Okta news, events, and job opportunities by joining our Talent Community.
We hope to connect soon!

Regards,

Okta"""
email7 = """Hi Jayden,
Thank you for applying to our role: University Software Engineer - Intern. We appreciate your interest in joining the team! We will review your application shortly. If you are given further consideration for any open positions, you will be contacted by our recruiting team.
All the best,
Crusoe"""
email8 = """Dear Jayden, 

Thank you very much for your recent application to the Computer Science Intern position at TRC Companies, Inc.. Your submission will be reviewed by our recruiting staff, and we may reach out to you for more information if we determine that your background meets our staffing needs.
 
Thank you again for your interest in our company.
 
Sincerely,
TRC Companies, Inc. """
email9 = """Thanks for applying to Amazon! We've received your application for the Systems Development Engineer Summer Internship – 2025 (US) (ID: 2739024) position.
If we decide to move forward with your application, the Amazon recruiting team will reach out to discuss next steps. Any updates to your application status will be reflected on your Application dashboard, so be sure to check back regularly."""
email10 = """Jayden,

Thanks for applying to Garda Capital Partners. Your application has been received and we will review it shortly.

If your application seems like a good fit for the position we will contact you soon.

Regards,
Garda Capital Partners"""
email11 = """Hi Jayden,

Thank you for your interest in a career at Tanium. We have received your application for the open Software Engineering Intern position. 

What happens now? We will review your resume and will contact you if there is a good match.  

Sincerely,
Tanium Recruiting Team"""
email12 = """Dear Jayden Thank you for your interest in Stryker! We have received your resume/CV for the R527618 Summer 2025 Intern - Software Engineering - Washington (Evergreen) position.

A member of our talent acquisition team will review your application and information and determine if there is a match between your resume and what the hiring team is looking for. Please be aware that it can take up to two weeks to receive an update from our team as we work to review applications. We are grateful for your patience as we determine candidacy.  

We appreciate your interest in pursuing Stryker for your next career move!

Sincerely,

Stryker's Talent Acquisition Team"""
email13 = """Dear Jayden,

Thank you for your interest in 2025 Software Engineer Program - Summer Internship (Code for Good Hackathon) - United States position. We're always looking for top talent and we're glad that you're considering us for your next role. If our team feels your skills and experience are a good fit for this opportunity, we'll reach out. 

And remember, you can always log back into your profile from the careers site homepage to view your status and if needed, withdraw your application.

We also invite you to visit our careers site to find and apply for other positions that match your skills and interests. 

We appreciate your interest in working with us!

Sincerely, 
JPMorgan Chase Recruiting"""
email14 = """Congratulations!

You've made an excellent choice by contacting  Currency. This email confirms that we have received your application. Should your background and experience meet the requirements of the position to which you've applied, we will be in contact.

Thank you for your interest in Crane NXT!

Sincerely,

Recruiting Team"""
email15 = """Dear Jayden Udall ,

Thank you for your application for the position Software Engineering Intern, Machine Learning (Summer 2025) and your interest in working at GLOBALFOUNDRIES.

Your application will be carefully reviewed by the responsible recruiter and the hiring department. Afterwards we will get back to you with information about the status of your application.

In the meantime, you can access your applicant profile at any time, from your Candidate Home: https://globalfoundries.wd1.myworkdayjobs.com/External
This e-mail box is not monitored. Please do not reply to this message."""
email16 = """Jayden,

Thank you for your interest in employment with Coffman Engineers, Inc.! We have received your application for 1505 Lyndon B Johnson Freeway, Suite 240, Dallas, TX, United States's Electrical Engineering Intern position. We are processing your resume and you will hear from us in the near future. 

If you created a SmartRecruiters account, you can check the status of your application online. Otherwise, expect further communication from us to be by email or phone. 

Please let us know if you have any questions by contacting us at careers@coffman.com!

Thank you.

Coffman Engineers, Inc."""
email17 = """JAYDEN,

Thank you for applying to our Intern - Software/Algorithm position, 2424729. We will review your profile and provide you with an update at our earliest opportunity. To check the status of your application, please visit our Career Site using the link provided below and log into your Workday Home Account to view status.

https://kla.wd1.myworkdayjobs.com/Search

Thank you for your interest in joining KLA.

Talent Acquisition Team"""
email18 = """Dear Jayden:
 
We have successfully received your submission to the following position(s):  Cybersecurity Intern - 4704. 
 
Your resume and screening answers will be carefully reviewed.  If your experience and skills match the requirements of this position, we will contact you with the next stage in our hiring process.
 
Thank you for your interest in employment at Ameritas."""
email19 = """Hello Jayden,

Thank you for your application! We are excited about your interest in joining BAE Systems to help protect those who protect us and innovate for those that move the world.

Over the coming weeks, our Talent Acquisition team will be evaluating applications for this role and will make contact with you should your application be compatible with the requirements.

In the meantime, you can the following links to stay in touch:

Check your application status and manage your profile

Get answers to frequently asked questions

Join our Talent Community to set up job alerts and receive career related news

Thank you,

BAE Systems Talent Acquisition Team"""
email20 = """Hi Udall,
Thanks for applying to our 2025 Charles Schwab Model Risk Internship 
(Artificial Intelligence, Machine Learning, Financial Engineering and Data Science), 2024-101928.
Our Talent Acquisition teams are working through the many applications Schwab receives and will 
reach out if you are selected for an interview."""
email21 = """Hi Udall,
 
Thank you again for considering Charles Schwab and the time you invested in applying. We have decided to pursue other candidates for this position. However, your talents and expertise may be better suited for other opportunities on our team.   
  
We invite you to stay connected by: 
Updating your Talent Network profile and requesting email notifications of new openings that match your profile description
Visiting our Careers Website to explore all current openings
Following us on LinkedIn
This declination only applies to this position: 2025 Charles Schwab Model Risk Internship (Artificial Intelligence, Machine Learning, Financial Engineering and Data Science), 2024-101928.
 
We wish you all of the best with your professional endeavors and hope you will consider applying for positions with us again in the future. """
email22 = """You are receiving this because you expressed interest in our Summer 2025 internships. The Lumen University Relations Team is gearing up to start our recruitment cycle in a few short weeks.

Curious about landing one of our sought-after intern spots? Join us on October 2nd at 4:00 CT for an informative session featuring insights from past interns and team recruiters. Save the date! The call invite will follow in two weeks.

Meanwhile, hear how this program has shaped previous interns' careers. This could be your future too!"""
email23 = """Hello Jayden,

Thank you for your interest in our Electrical Engineering Internship opening. We have reviewed your resume and unfortunately, we have decided to pursue other candidates who appear to match our requirements (skills and experience) more closely at this time.

Thank you again for your interest in an employment opportunity with Sparton Corporation, and we wish you the best in your job search.
 
 
 
Respectfully,
 
Talent Acquisition"""
email24 = """Jayden,

Thanks for taking the time to apply at Hudl—we know the application process takes time and effort. Right now, we've decided to move forward with other candidates for the open Software Engineer Intern role at Hudl. A lot of talented people applied for this position and we've had to make some (very) tough decisions like this one.

We really do appreciate your interest in Hudl, and we want to wish you the best of luck in your job search.

Thanks, Jayden."""
email25 = """Hello,
Your BenefitsCal verification code is: xxxxxx.
Please enter this code in the next 15 minutes.
Please do not reply to this email. It has been automatically generated and replies will go to an unattended inbox.
If you have any questions, contact your local office.
Thank you,
BenefitsCal"""
email26 = """Hi Jayden,
Starting out in today’s job market can feel overwhelming. How do you stand out, seize the right opportunities and accelerate your career? Virgin Group Founder Richard Branson has built a global empire by doing just that — turning bold ideas into groundbreaking successes across industries like music, aviation and space travel. 

You’re invited to ask Branson your career questions live during an exclusive conversation with LinkedIn Editor in Chief Daniel Roth on Tuesday, Sept. 24."""
email27 = """In 2014, Wizkid released “Ojuelegba” - a retrospective track that pays tribute to his neighbourhood "Ojuelegba" - a small township in Lagos and his rise to fame from humble beginnings.
Until date, Ojuelegba is considered a modern African classic, and an anthem of hope."""
email28 = """Hi Jayden,
 

While we're reviewing your application for the Engineering Intern - Electrical (Summer 2025) position, we'd love to hear about your experience so far! Our team is continuously working to improve our candidate experience and your feedback plays an important role in that process.

 

Please take a moment to complete a short 5-question survey about our application process. All feedback is anonymous and not associated with any application. Participating in this survey is voluntary and will not impact potential employment with Oshkosh or any of its leading brands"""
email29 = """We’ve updated the Steam Subscriber Agreement. The updates affect your legal rights. They include changes to how disputes and claims between you and Valve are resolved. The updated dispute resolution provisions are in Section 10 and require all claims and disputes to proceed in court and not in arbitration. We’ve also removed the class action waiver and cost and fee-shifting provisions. Please carefully review the updated Steam Subscriber Agreement here."""
email30 = """Your subscription from Google LLC on Google Play continues and you've been charged. Manage your subscriptions

To help keep your subscription active, add a backup payment method."""
email31 = """Hi Udall,
 
Thank you again for considering Charles Schwab and the time you invested in applying. We have decided to pursue other candidates for this position. However, your talents and expertise may be better suited for other opportunities on our team.   
  
We invite you to stay connected by: 
Updating your Talent Network profile and requesting email notifications of new openings that match your profile description
Visiting our Careers Website to explore all current openings
Following us on LinkedIn
This declination only applies to this position: 2025 Charles Schwab Model Risk Internship (Artificial Intelligence, Machine Learning, Financial Engineering and Data Science), 2024-101928.
 
We wish you all of the best with your professional endeavors and hope you will consider applying for positions with us again in the future. """
email32 = """You are receiving this because you expressed interest in our Summer 2025 internships. The Lumen University Relations Team is gearing up to start our recruitment cycle in a few short weeks.

Curious about landing one of our sought-after intern spots? Join us on October 2nd at 4:00 CT for an informative session featuring insights from past interns and team recruiters. Save the date! The call invite will follow in two weeks.

Meanwhile, hear how this program has shaped previous interns' careers. This could be your future too!"""
email33 = """Hello Jayden,

Thank you for your interest in our Electrical Engineering Internship opening. We have reviewed your resume and unfortunately, we have decided to pursue other candidates who appear to match our requirements (skills and experience) more closely at this time.

Thank you again for your interest in an employment opportunity with Sparton Corporation, and we wish you the best in your job search.
 
 
 
Respectfully,
 
Talent Acquisition"""
email34 = """Jayden,

Thanks for taking the time to apply at Hudl—we know the application process takes time and effort. Right now, we've decided to move forward with other candidates for the open Software Engineer Intern role at Hudl. A lot of talented people applied for this position and we've had to make some (very) tough decisions like this one.

We really do appreciate your interest in Hudl, and we want to wish you the best of luck in your job search.

Thanks, Jayden."""
email35 = """Hello,
Your BenefitsCal verification code is: xxxxxx.
Please enter this code in the next 15 minutes.
Please do not reply to this email. It has been automatically generated and replies will go to an unattended inbox.
If you have any questions, contact your local office.
Thank you,
BenefitsCal"""
email36 = """Hi Jayden,
Starting out in today’s job market can feel overwhelming. How do you stand out, seize the right opportunities and accelerate your career? Virgin Group Founder Richard Branson has built a global empire by doing just that — turning bold ideas into groundbreaking successes across industries like music, aviation and space travel. 

You’re invited to ask Branson your career questions live during an exclusive conversation with LinkedIn Editor in Chief Daniel Roth on Tuesday, Sept. 24."""
email37 = """In 2014, Wizkid released “Ojuelegba” - a retrospective track that pays tribute to his neighbourhood "Ojuelegba" - a small township in Lagos and his rise to fame from humble beginnings.
Until date, Ojuelegba is considered a modern African classic, and an anthem of hope."""
email38 = """Hi Jayden,
 

While we're reviewing your application for the Engineering Intern - Electrical (Summer 2025) position, we'd love to hear about your experience so far! Our team is continuously working to improve our candidate experience and your feedback plays an important role in that process.

 

Please take a moment to complete a short 5-question survey about our application process. All feedback is anonymous and not associated with any application. Participating in this survey is voluntary and will not impact potential employment with Oshkosh or any of its leading brands"""
email39 = """We’ve updated the Steam Subscriber Agreement. The updates affect your legal rights. They include changes to how disputes and claims between you and Valve are resolved. The updated dispute resolution provisions are in Section 10 and require all claims and disputes to proceed in court and not in arbitration. We’ve also removed the class action waiver and cost and fee-shifting provisions. Please carefully review the updated Steam Subscriber Agreement here."""
email40 = """Your subscription from Google LLC on Google Play continues and you've been charged. Manage your subscriptions

To help keep your subscription active, add a backup payment method."""


emails = [email1, email2, email3, email4, email5, email6, email7, email8, email9, email10,
    email11, email12, email13, email14, email15, email16, email17, email18, email19, email20,
    email21, email22, email23, email24, email25, email26, email27, email28, email29, email30,
    email31, email32, email33, email34, email35, email36, email37, email38, email39, email40
]
labels = ['confirmation', 'confirmation', 'confirmation', 'confirmation', 
          'confirmation', 'confirmation', 'confirmation', 'confirmation', 
          'confirmation', 'confirmation', 'confirmation', 'confirmation', 
          'confirmation', 'confirmation', 'confirmation', 'confirmation', 
          'confirmation', 'confirmation', 'confirmation', 'confirmation', 
          'not confirmation', 'not confirmation', 'not confirmation', 'not confirmation', 
          'not confirmation', 'not confirmation', 'not confirmation', 'not confirmation', 
          'not confirmation', 'not confirmation', 'not confirmation', 'not confirmation',
          'not confirmation', 'not confirmation', 'not confirmation', 'not confirmation',
          'not confirmation', 'not confirmation', 'not confirmation', 'not confirmation',
]

vectorizer = TfidfVectorizer(stop_words=None)
features = vectorizer.fit_transform(emails)



X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42 )

classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)

with open('tfidf_vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)
with open('email_classifier.pkl', 'wb') as model_file:
    pickle.dump(classifier, model_file)
classifier_check = None
if os.path.exists('email_classifier.pkl'):
    with open('email_classifier.pkl', 'rb') as model_file:
        classifier_check = pickle.load(model_file)
if classifier_check is not None:
    print (f"model found")
else:
    print(f"model not found")
if classifier is not None:

    y_pred = classifier.predict(X_test)
    print(f"Accuracy score: {accuracy_score(y_test, y_pred)}")

#email list data
