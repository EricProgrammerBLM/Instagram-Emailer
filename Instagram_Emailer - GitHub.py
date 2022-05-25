from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import os
import base64
import re
import random
from Instagram_Email_API import GrabAPI_Usernames, UpdateAPI_Usernames 
#^ API Functions I built from Instagram_Email_API.py

#---------- Email Variables Being Sent
Subject = 'Subject Line for the Email Goes Here'
Email = "Full Email Body Goes Here"


#------------- List & Variables Below
Buttons = []           #User to hold the text string for Email or Contact
Contact = []
Bounds_List = []       #To hold the last value of the bounds for each username and tagged name so its easier for the bot to click
Everyone = []          #List of every page we have ever visited whether we sent them an email or not
Page_Text = []         #List to hold all the text on the page
Usernames = []         #This list is for the name of the @ name that left the comment
Contacted = []         #Will Be for @Names we've already Contacted via Email. If they're in this list the bot will skip over them.
AmountOfButtons = []   #Used to hold the amount of buttons on a page to determine if a page is public or not
ContactedEms = []      #Will Be for @Names EMAILS we've already Contacted. If they're in this list the bot will skip over them as well
ProfilesOfInterest = []#This list will be a combo of both @ names mentioned and @ names commented; Purposely should reset after its function use
PersonTagged = []      #This list will have the tagged @ names comment being focused on; This way we can use it as a way to make an xpath and click on their profile
Bio_Emails = []        #This will be used to hold the EmailsSents that aren't in a contact button but are in peoples bio's
keywords = ['unitedmasters', 'spotify', 'mixtapes','rapper', 'musician','a r t i s t', 'label', 'artist', 'singer', 'song', 'song writer', 'feature', 'youtu', 'youtube.', 'soundcloud', 'linktr.ee', 'music', 'apple', 'li.sten', 'distrokid']
Screenshot_Random_Names = ['1', '2', '3', '4','5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
Screenshot_Random_Names2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 't', 'u', 'ii', 'a']
Comment_Order = 1      #The 1st Comment in any Comment Section has a Class of android.widget.LinearLayout[2]; As we filter each comment we'll have to increase this by 1
Points = 0             #Point system to determine of the profile is an artist/rapper
MegaSwipe = 0          #This var will be used to determine if a comment has been emailed already days ago and added to the list, so it will perform a mega swipe
EmailsSent = 0
print ('Also for the Saved Post XPATH remember, to change the order of how its picked just change the number at the very end')
print ('Still have to filter the ProfileOfInterest for Duplicates')
print ('Add Screen Shot Function where if points 5 or less, saved to No Email Sent Folder')
print ('For Mega Swipe do Cordinates')
print ('Find the difference between disabled pages and private and public pages')



#------------- Locators - XPATH's, ID's etc Below:
#Comment_XPATH = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout["+Comment_Order+"]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView"
SavedPost_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]'
#^ At the end just replace the 1 with 2 or 3 if you want to changed

#Self Explanatory
IG_Bio_ID = "com.instagram.android:id/profile_header_bio_text"
IG_Bio_Website_Link_ID = "com.instagram.android:id/profile_header_website"
IG_Bio_Page_Category_ID = "com.instagram.android:id/profile_header_business_category"
IG_Profile_Name_ID = "com.instagram.android:id/profile_header_full_name"
IG_Buttons_ID = 'com.instagram.android:id/button_text'
IG_Buttons_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.Button'
            


#-------------- Desired Capabilities

desired_cap = {
    "deviceName": "R9AN60B4CCJ",
    "platformName": "Android",
    "app": "C:\\Users\\John Doe\\Downloads\\Instagram.apk",
    "appPackage": " com.instagram.android",
    "appActivity": "com.instagram.mainactivity.MainActivity", 
    "newCommandTimeout": 30000 #Prevents the app from closing after 60 seconds of being idle

    #adb shell "dumpsys window | grep mCurrentFocus"    <-- Copy & Paste into CMD
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_cap)
driver.implicitly_wait(100)
#Clicking our way to the saved post on Instagram; may record this later in the desired capabilities
driver.find_element(By.ID, 'com.instagram.android:id/tab_avatar').click()
sleep(2)
driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="Options"]').click()
sleep(1)
driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="Saved"]').click()
#Used the tap feature, App Source inside Inspector said it wasn't clickable, although I didn't even try.
#TouchAction(driver).tap(x=183, y=352).perform()
sleep(1)
TapOnPhone = TouchAction(driver)
TapOnPhone.tap(None, 183, 352, 1).perform() #Does a single tap this time with 1 as the duration; When it was 5 it did a double tap...
driver.implicitly_wait(100)
sleep(2)
driver.find_element(By.XPATH, (SavedPost_XPATH)).click();
#Clicks on one of your saved post depending on the Row and Column Number. Will Create Variables for those later
driver.find_element(By.ID, 'com.instagram.android:id/row_feed_button_comment').click()
sleep(2) #^ Clicks on the comment button to see the Comment Section
driver.hide_keyboard()
driver.implicitly_wait(100)


#driver.start_recording_screen()

def SendAnEmail(var):
    global EmailsSent
    if var == 'Contact': #             //android.widget.Button[@resource-id='com.instagram.android:id/button_text' and contains(@text,'Contact')]
        driver.find_element(By.XPATH, "//android.widget.Button[@resource-id='com.instagram.android:id/button_text' and contains(@text,'Contact')]").click() #Should Click on the Contact Button, Gotta fix this and make this Generic
        driver.implicitly_wait(50)
        sleep(4)
        Contact_Option = driver.find_element(By.XPATH, ' /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.TextView[1]').text
        Contact_Details = driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.TextView[2]').text
        Contact2_Option = driver.find_element(By.XPATH, ' /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.TextView[1]').text
        Contact2_Details = driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.TextView[2]').text
        if Contact_Option == 'Email' and '@' in Contact_Details:
           driver.implicitly_wait(50)
           driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]').click() #These need to be fixed
           driver.implicitly_wait(50)
           driver.find_element(By.ID, 'com.google.android.gm:id/subject').send_keys(Subject) #The Subject
           driver.find_element(By.XPATH, '//android.widget.EditText[contains (@bounds, "694,")]').send_keys(Email)
           driver.find_element(By.ID, 'com.google.android.gm:id/send').click()
           print ('Email Sent')
           EmailsSent = EmailsSent + 1
        elif Contact2_Option == 'Email' and '@' in Contact2_Details:
            driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]').click() # These need to be fixdd
            driver.implicitly_wait(50)
            driver.find_element(By.ID, 'com.google.android.gm:id/subject').send_keys(Subject) #The Subject
            driver.find_element(By.XPATH, '//android.widget.EditText[contains (@bounds, "694,")]').send_keys(Email)
            driver.find_element(By.ID, 'com.google.android.gm:id/send').click()
            print ('Email Sent')
            EmailsSent = EmailsSent + 1
        elif Contact2_Option == 'Request email' or Contact_Option == 'Request email': #Sometimes profiles dont have the emails listed, so this will prevent it from going into the person's DM
            print ('No Email Listed on the Account')
    elif var == 'Email':
        driver.find_element(By.XPATH, "//android.widget.Button[@resource-id='com.instagram.android:id/button_text' and contains(@text,'Email')]").click()
        driver.implicitly_wait(50)
        driver.find_element(By.ID, 'com.google.android.gm:id/subject').send_keys(Subject) #The AkSubject
        driver.find_element(By.XPATH, '//android.widget.EditText[contains (@bounds, "694,")]').send_keys(Email)
        driver.find_element(By.ID, 'com.google.android.gm:id/send').click()
        print ('Email Sent')
        EmailsSent = EmailsSent + 1

def CheckTheProfile(pointsystem, buttonslist, keywordlist, commentSectionAtNamesList, boundss, thebackfunction, emailfunction, ScreenShotEmailStringName): #<------ have to add email function here too
    try:
        Profile_Cat = driver.find_element(By.ID, IG_Bio_Page_Category_ID).text 
        Profile_Cat = Profile_Cat.lower()
        if any(word in Profile_Cat for word in keywordlist):
            pointsystem += 1
            print (Profile_Cat)
    except NoSuchElementException:
        print ('No Category In His Bio...')

    
    try:
        Bio = driver.find_element(By.ID, IG_Bio_ID).text 
        Bio = Bio.lower() 
        if any(word in Bio for word in keywordlist):
            pointsystem += 1
            print (Bio)
    except NoSuchElementException:
        print ('No Bio.....')

    try:
        Link = driver.find_element(By.ID, IG_Bio_Website_Link_ID).text 
        Link = Link.lower() 
        if any(word in Link for word in keywordlist):
            pointsystem += 1
            print (Link)
    except NoSuchElementException:
        print ('No Link In His Bio...')

    Button = driver.find_elements(By.ID, IG_Buttons_ID)
    for i in Button:
        if 'Contact' == (i.text) or 'Email' == (i.text): #Searchs the profile for an Email button or Contact Button
            pointsystem += 5
            Buttons.append(i.text)
            Communication = (i.text)
    #if pointsystem < 5:
    print (Buttons)
    print (pointsystem)
    print (commentSectionAtNamesList[0])
    print (boundss[0])
    if pointsystem < 6:
        commentSectionAtNamesList.remove(commentSectionAtNamesList[0])
        boundss.remove(boundss[0])
        Buttons.clear()
        thebackfunction()
        driver.implicitly_wait(20)
        sleep(1)
        return (commentSectionAtNamesList, Buttons, boundss)
    else: 
        emailfunction(Communication)
        driver.find_element(By.ID, 'com.instagram.android:id/action_bar_title').click() #Recently put here, only to get the screen out of the contact pop up menu after email is sent
        driver.save_screenshot('/Users/John Doe/Dropbox/Business/Methods/Data/Email Bot Screenshots/Sent Email/' + ScreenShotEmailStringName + '.png')
        Buttons.clear()
        commentSectionAtNamesList.remove(commentSectionAtNamesList[0])
        boundss.remove(boundss[0])
        thebackfunction()
        driver.implicitly_wait(20)
        sleep(1)
        return (commentSectionAtNamesList, Buttons, boundss)

def FilterForEmojis(string):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', string)
    return (text)

def CommentSection(filter_emojis):
    driver.implicitly_wait(100)
    Comment = driver.find_element(By.XPATH, "//android.widget.TextView[contains(@content-desc,'said')]").text 
    print('')
    print (Comment)
    print('')
    global MegaSwipe
    global ProfilesOfInterest 
    Usernames.append(Comment.split()[0]) #         The Username that left the comment will be added to this list
    ProfilesOfInterest.append(Comment.split()[0]) #Helps us know how many names to click on per potentially comment to send an email too
    for taggedname in Comment.split():
        if '@' in taggedname and taggedname[0] == '@':
            PersonTagged.append(taggedname) #      Anybody that was tagged in the comment will be added to this list
            ProfilesOfInterest.append(taggedname)

    #Gets rid of duplicates from a comment section
    ProfilesOfInterest = list(set(ProfilesOfInterest))

    #Filters and Takes Emojis out of Names
    for taggedname in ProfilesOfInterest[0:]:
        ProfilesOfInterest.remove(taggedname)
        ProfilesOfInterest.append(filter_emojis(taggedname))

    #Keep Us from Visiting Page's we've already been to before
    for names in Everyone:
        if names in ProfilesOfInterest:
            ProfilesOfInterest.remove(names)
    print (ProfilesOfInterest)
    MegaSwipe = len(ProfilesOfInterest)

    return (Usernames, ProfilesOfInterest, PersonTagged, Everyone) #Passes the value outside of this function

def AccountPrivacy(allthepagebuttonslist):
    Page = driver.find_elements(By.XPATH, IG_Buttons_XPATH)
    for amount_of_buttons_on_the_page in Page:
        allthepagebuttonslist.append(amount_of_buttons_on_the_page)
    print ('Amount of Buttons on the Page: ', len(allthepagebuttonslist)) #Private Pages have 1 Follow Button; Public Pages have 2 or More, this Function helps the bot Determine that
    return (allthepagebuttonslist)

def SwipeTheCommentSectionUp(usernames_list, megasuperswipe): #Might have to use peoples usernames instead as a swipe option
    el1 = driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="'+ usernames_list[-1] +'"]') #@resource-id='com.instagram.android:id/row_comment_container' and
    el2 = driver.find_element(By.XPATH, "//android.widget.LinearLayout[contains(@index,'2')]") #^Took that out of the brackets; Could also make el1 use Usernames[-1]
    el3 = driver.find_element(By.XPATH, "//android.widget.LinearLayout[contains(@index,'3')]")
    Scroll = TouchAction(driver)
    if (megasuperswipe) == 0:
        Scroll.press(el3).move_to(el1).release().perform()
        print ('Mega Swiped! Comments been hit before!')
    elif (megasuperswipe) >= 1:
        Scroll.press(el2).move_to(el1).release().perform()
        print ('Scrolling Now..')
    
def BackButton():
    driver.implicitly_wait(25)
    if (driver.find_element(By.ID, 'com.instagram.android:id/action_bar_title').text) != 'Comments':
        driver.find_element(By.ID, 'com.instagram.android:id/action_bar_button_back').click()
        print ('Stuck in the Comment Section')
    elif (driver.find_element(By.ID, 'com.instagram.android:id/action_bar_title').text) == '1 selected':
        driver.find_element(By.ID, 'com.instagram.android:id/action_bar_button_back').click()
        print ('Comment Selected, Popped Up')
    elif (driver.find_element(By.ID, 'com.instagram.android:id/action_bar_title').text) == 'Comments':
        print ('This is the Comment Section')
        #Reason for this function, it checks to make sure the profile is even
        #clicked on before it hits the back button, reason being, sometimes the program
        #Thinks it clicked on the profile, but didnt and instead is still in the comment section.
        #Then it ends up backing out of the comment section

Everyone = GrabAPI_Usernames(Everyone)
#Grabs the list of Profile Usernames we have already visited in the past already.

Scroll = TouchAction(driver)
Scroll.press(x=360, y=525).move_to(x=360, y=241.5).release().perform()
#So the bot doesn't confuse the Caption as a comment, we scroll down and take it out of view
#print ('Activating')
#sleep(10)

           

while True:
    random.shuffle(Screenshot_Random_Names)
    random.shuffle(Screenshot_Random_Names2)
    Email = 'Email Sent' + Screenshot_Random_Names[0] + Screenshot_Random_Names2[0]
    Public = 'Public Account' + Screenshot_Random_Names[0] + Screenshot_Random_Names2[0]
    Private = 'Private Account' + Screenshot_Random_Names[0] + Screenshot_Random_Names2[0]
    BackButton() 
    CommentSection(FilterForEmojis)
    for names in ProfilesOfInterest: #Filters and Updates the Global List of names we've seen before; that list would be Everyone. We sill send that info to the API
        if names in Everyone:
            ProfilesOfInterest.remove(names)
        elif names not in Everyone:
            Everyone.append(names)

    for a in ProfilesOfInterest: #Just gets bounds of each name we're going to click on after its been filtered; Currently has no use but may use later
        targets_bounds = driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="'+ a +'"]').get_attribute('bounds')
        Bounds_List.append(targets_bounds)
        print ('Bounds Added to the List: ', targets_bounds)
        #sleep(99900)

    while len(ProfilesOfInterest) != 0:
        driver.implicitly_wait(100)
        Profile_XPATH = '//android.widget.Button[@content-desc="'+ ProfilesOfInterest[0] +'"]'
        ProfileOrComments = driver.find_element(By.ID, 'com.instagram.android:id/action_bar_title').text #This ID will tell the bot whether its a comment section or profile
        while (driver.find_element(By.ID, 'com.instagram.android:id/action_bar_title').text) == 'Comments':
            driver.find_element(By.XPATH, Profile_XPATH).click() 
            print ('Clicked on Profile: ', ProfilesOfInterest[0])
            driver.implicitly_wait(100)
            ProfileOrComments = driver.find_element(By.ID, 'com.instagram.android:id/action_bar_title').text #This ID will tell the bot whether its a comment section or profile
            if ProfileOrComments == 'Comments':
                print (ProfileOrComments)
                Scroll.press(x=360, y=241.5).move_to(x=360, y=350).release().perform()
                driver.implicitly_wait(100)
                driver.find_element(By.XPATH, Profile_XPATH).click() 
                print ('Clicked on Profile Again: ', ProfilesOfInterest[0])
            else: 
                print ('On Profile: ', ProfileOrComments)

        AccountPrivacy(AmountOfButtons)
        try:
            Follow_Button_Bounds = driver.find_element(By.XPATH, '//android.widget.Button[contains(@content-desc, "Follow")]').get_attribute('bounds')
            print ('Follow Button Bound: ', Follow_Button_Bounds)
        except NoSuchElementException:
            print ('Most Likely a Disabled Page...')
            
        if (len(AmountOfButtons)) <= 2 or '320,' in Follow_Button_Bounds or '355,' in Follow_Button_Bounds: #---- PRIVATE OR PUBLIC? This IF STATEMENT Determines That;  
            ProfilesOfInterest.remove(ProfilesOfInterest[0])
            Bounds_List.remove(Bounds_List[0])
            print ('Account is Private or Has No Email')
            driver.save_screenshot('/Users/John Doe/Dropbox/Business/Methods/Data/Email Bot Screenshots/Private Page/' + Private + '.png')
            print ('')
            AmountOfButtons.clear()
            BackButton() #This fixes the error by accident because, sometimes we get a selected pop up that blocks the 'Comments' Header.
        elif '217,' in Follow_Button_Bounds or '240,' in Follow_Button_Bounds or '[699,' in Follow_Button_Bounds:
            print ('Account is Public')
            driver.save_screenshot('/Users/John Doe/Dropbox/Business/Methods/Data/Email Bot Screenshots/Public Page/' + Public + '.png')
            print ('')
            AmountOfButtons.clear()
            CheckTheProfile(Points, Buttons, keywords, ProfilesOfInterest, Bounds_List, BackButton, SendAnEmail, Email) 
            print ('') 
    print ('ProfilesOfInterest List: ', ProfilesOfInterest)
    print ('Bounds List: ', Bounds_List)
    Comment_Order += 1 
    print ('Mega Swipe: ', MegaSwipe)
    SwipeTheCommentSectionUp(Usernames, MegaSwipe)
    MegaSwipe = 0
    print ('New Mega Swipe: ', MegaSwipe)
    print ('On Comment: ', Comment_Order)
    print ('')
    print ('Emails Sent: ', EmailsSent)
    #print ('Global List Updated: ', Everyone)
    print ('Global List Updated!')
    print('')
    UpdateAPI_Usernames(Everyone)
    print ('--------------------------------------')
    print ('')
    if EmailsSent == 150: #Amount of emails we would like the bot to completely stop at
        sleep(99999)
    




    
