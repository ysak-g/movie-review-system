'''
Movie Rreview system
'''

from flask import Flask
from flask import request
import csv
import json
import time
import jwt


app = Flask(__name__)

#function for user registration
@app.route('/user/register',methods=['POST'])
def user_registration():
    user_name = request.json['user_name']
    password = request.json['password']
    email = request.json['email']
    contact_number = request.json['contact_number']
    address = request.json['address']
    new_user = True
    with open('data/user.csv','r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['name'].lower() == user_name.lower():
                new_user = False
                break
    if new_user:
        user_list = {}
        with open('data/user.csv','r') as users_file:
            csv_reader = csv.reader(users_file)
            data = list(csv_reader)
        u_id = data[-1][0]
        #id automatically generating with respect to previous
        user_list['id'] = int(u_id) + 1
        user_list['name'] = user_name
        user_list['password'] = password
        user_list['contact_number'] = contact_number
        user_list['address'] = address
        with open('data/user.csv','a') as users_file2:
            headers = ['id','name','email','password','contact_number','address']
            csv_writer = csv.DictWriter(users_file2,fieldnames=headers)
            csv_writer.writerow(user_list)
        return json.dumps({"message":"User Added Successfully"})
    else:
        return json.dumps({"message":"User name already exists!"})

#function for user login
@app.route('/user/login',methods=['POST'])
def user_login():
    user_name = request.json['user_name']
    password = request.json['password']
    with open('data/user.csv','r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        valid_user = False
        output_message = ''
        for row in csv_reader:
            # print(row['user_name'].lower())
            if row['name'].lower() == user_name.lower() and row['password'] == password:
                valid_user = True
                user_id = row['id']
                output_message = "Login Successful"
                break
            else:
                output_message = "User name or password is not matching"
    if valid_user:
        payload = {'username':user_name,'user_id':user_id,'expire':time.time()+3600}
        key = "movie"
        encode_jwt = jwt.encode(payload,key)
        return {'auth_token':encode_jwt.decode(),'message':output_message}
    else:
        return json.dumps({"message":output_message})

#function for user modify
@app.route('/user/modify',methods=['PATCH'])
def modify_user():
    user_id = request.json['id']
    password = request.json['password']
    auth_token = request.json['auth_token']
    key = "movie"
    data = jwt.decode(auth_token,key)
    if data['user_id'] == user_id and data['expire'] >= time.time():
        with open('data/user.csv','r') as users_file:
            csv_reader = csv.reader(users_file)
            data = list(csv_reader)
            for i in range(len(data)):
                if data[i][0] == user_id:
                    data[i][0] = user_id
                    data[i][3] = password
        with open('data/user.csv','w') as csv_file:
            csv_writer =  csv.writer(csv_file)
            csv_writer.writerows(data)
        return json.dumps({"message":"Password Updated Succesfully"})
    else:
        if data['user_id'] != user_id:
            return json.dumps({"message":"Invalid user"})
        else:
            return json.dumps({"message":"Session expired"})

#function to delete a user
@app.route('/user/delete',methods=['DELETE'])
def delete_user():
    user_id = request.json['user_id']
    auth_token = request.json['auth_token']
    key = "movie"
    data = jwt.decode(auth_token,key)
    print(data['user_id'])
    if data['user_id'] == "1" and data['expire'] >= time.time():
        new_list = []
        with open('data/user.csv','r') as csv_file:
            csv_reader = csv.reader(csv_file)
            lines = list(csv_reader)
            for i in range(len(lines)):
                if i != int(user_id):
                    new_list.append(lines[i])
        with open('data/user.csv','w') as csv_file2:
            csv_writer = csv.writer(csv_file2)
            csv_writer.writerows(new_list)
        return json.dumps({"message":"User Deleted Successfully!"})
    else:
        if data['user_id'] != "1":
            return json.dumps({"message":"Only admin have the previlage to delete a user"})
        else:
            return json.dumps({"message":"Session expired"})

#show all users
@app.route('/users/view',methods=['GET'])
def view_users():
    user_list = []
    with open('data/user.csv','r') as users_file:
        csv_reader = csv.DictReader(users_file)
        for row in csv_reader:
            user_list.append(row)
        return json.dumps({"users":user_list})

#Add movies
@app.route('/movie/create',methods=['POST'])
def add_movie():
    auth_token = request.json['auth_token']
    movie_name = request.json['movie_name']
    year = request.json['year']
    duration = request.json['duration']
    user_id = request.json['user_id']
    key = "movie"
    data = jwt.decode(auth_token,key)
    if data['expire'] >= time.time():
        with open('data/movies.csv','r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            movie_list = {}
            with open('data/movies.csv','r') as users_file:
                csv_reader = csv.reader(users_file)
                data = list(csv_reader)
            u_id = data[-1][0]
            movie_list['id'] = int(u_id) + 1
            movie_list['movie_name'] = request.json['movie_name']
            movie_list['year'] = request.json['year']
            movie_list['duration'] = request.json['duration']
            movie_list['user_id'] = request.json['user_id']
            with open('data/movies.csv','a') as users_file2:
                headers = ['id','movie_name','year','duration','user_id']
                csv_writer = csv.DictWriter(users_file2,fieldnames=headers)
                csv_writer.writerow(movie_list)
            return json.dumps({"message":"Movie Added Successfully"})
    else:
        return json.dumps({"message":"Session expired!"})

#Add comments
@app.route('/comments/add',methods=['POST'])
def add_comments():
    auth_token = request.json['auth_token']
    movie_id = request.json['movie_id']
    comment = request.json['comment']
    user_id = request.json['user_id']
    key = "movie"
    data = jwt.decode(auth_token,key)
    if data['expire'] >= time.time():
        with open('data/comments.csv','r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            movie_list = {}
            with open('data/comments.csv','r') as users_file:
                csv_reader = csv.reader(users_file)
                data = list(csv_reader)
            u_id = data[-1][0]
            movie_list['id'] = int(u_id) + 1
            movie_list['comment'] = request.json['comment']
            movie_list['movie_id'] = request.json['movie_id']
            movie_list['user_id'] = request.json['user_id']
            with open('data/comments.csv','a') as users_file2:
                headers = ['id','comment','movie_id','user_id']
                csv_writer = csv.DictWriter(users_file2,fieldnames=headers)
                csv_writer.writerow(movie_list)
            return json.dumps({"message":"Comment Added Successfully"})
    else:
        return json.dumps({"message":"Session expired!"})

#Add categories
@app.route('/category/add',methods=['POST'])
def add_categories():
    auth_token = request.json['auth_token']
    category_name = request.json['category_name']
    key = "movie"
    data = jwt.decode(auth_token,key)
    if data['expire'] >= time.time():
        with open('data/category.csv','r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            movie_list = {}
            with open('data/category.csv','r') as users_file:
                csv_reader = csv.reader(users_file)
                data = list(csv_reader)
            u_id = data[-1][0]
            movie_list['id'] = int(u_id) + 1
            movie_list['category_name'] = request.json['category_name']
            with open('data/category.csv','a') as users_file2:
                headers = ['id','category_name']
                csv_writer = csv.DictWriter(users_file2,fieldnames=headers)
                csv_writer.writerow(movie_list)
            return json.dumps({"message":"Category Added Successfully"})
    else:
        return json.dumps({"message":"Session expired!"})

#View Movies
@app.route('/movie/view',methods=['GET'])
def view_movie():
    bus_list = []
    with open('data/movies.csv','r') as users_file:
        csv_reader = csv.DictReader(users_file)
        for row in csv_reader:
            bus_list.append(row)
        return json.dumps({"movies":bus_list})

#View comments
@app.route('/comments/view',methods=['GET'])
def view_comments():
    bus_list = []
    with open('data/comments.csv','r') as users_file:
        csv_reader = csv.DictReader(users_file)
        for row in csv_reader:
            bus_list.append(row)
        return json.dumps({"comments":bus_list})

#View categories
@app.route('/categories/view',methods=['GET'])
def view_categories():
    bus_list = []
    with open('data/category.csv','r') as users_file:
        csv_reader = csv.DictReader(users_file)
        for row in csv_reader:
            bus_list.append(row)
        return json.dumps({"categories":bus_list})

#Search a movie
@app.route('/movie/search',methods=['POST'])
def search_movie():
    movie_name = request.json['movie_name']
    category_name = request.json['category_name']
    movie_found = False
    movie_details = {}
    # print(movie_name)
    with open('data/movies.csv','r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # print(row['movie_name'].lower())
            if row['movie_name'].lower() == movie_name.lower():
                movie_details['id'] = row['id']
                movie_details['movie_name'] = row['movie_name']
                movie_details['year'] = row['year']
                movie_details['duration'] = row['duration']
                movie_details['user_id'] = row['user_id']
                movie_found = True
                break
    if movie_found == True:
        return json.dumps({"movie detail":movie_details})
    else:
        return json.dumps({"message":"Movie not found!"})

#delete a movie
@app.route('/movie/delete',methods=['DELETE'])
def delete_movie():
    movie_id = request.json['movie_id']
    auth_token = request.json['auth_token']
    key = "movie"
    data = jwt.decode(auth_token,key)
    if data['expire'] >= time.time():
        new_list = []
        with open('data/movies.csv','r') as csv_file:
            csv_reader = csv.reader(csv_file)
            lines = list(csv_reader)
            for i in range(len(lines)):
                if lines[i][0] != movie_id:
                    new_list.append(lines[i])
        with open('data/movies.csv','w') as csv_file2:
            csv_writer = csv.writer(csv_file2)
            csv_writer.writerows(new_list)
        return json.dumps({"message":"Movie Deleted Successfully!"})
    else:
        return json.dumps({"message":"Session time out"})

#Modify Movie details
@app.route('/movie/modify',methods=['PATCH'])
def modify_movie():
    auth_token = request.json['auth_token']
    key = "movie"
    data = jwt.decode(auth_token,key)
    if data['expire'] >= time.time():
        movie_id = request.json['movie_id']
        movie_name = request.json['movie_name']
        year = request.json['year']
        duration = request.json['duration']
        user_id = request.json['user_id']
        with open('data/movies.csv','r') as users_file:
            csv_reader = csv.reader(users_file)
            data = list(csv_reader)
            for i in range(len(data)):
                if data[i][0] == movie_id:
                    data[i][0] = movie_id
                    data[i][1] = movie_name
                    data[i][2] = year
                    data[i][3] = duration
                    data[i][4] = user_id
        with open('data/movies.csv','w') as csv_file:
            csv_writer =  csv.writer(csv_file)
            csv_writer.writerows(data)
        return json.dumps({"message":"Movie Details Updated Succesfully"})
    else:
        return json.dumps({"message":"Session timeout!"})
