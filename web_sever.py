# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 16:04:55 2023

@author: lucas
"""

import socket
import os

# HTTP Status
STATUS200 = "200 OK"
STATUS301 = "301 Moved Permanently"
STATUS401 = "401 Unauthorized"
STATUS400 = "400 Bad Request"
STATUS404 = "404"
STATUS505 = "505 HTTP Version Not Supported"

def HTML_list_merge( request_list ) :
    html_list = []
    html_str = ''
    head_and_tail = 0
    
    while ( head_and_tail < 2 ) :
        take = request_list.pop()
        
        html_list.append( take )
        
        if take == '' :
            head_and_tail += 1
            
    html_list.reverse()
    
    for line in html_list :
        html_str = html_str + "\r\n" + line
    
    request_list.append( html_str )
    print( request_list )
    return request_list

def HTTP_Bad_Request( request ) :
    response = request[0].split(' ')[2] + ' ' + STATUS400 # error message
    response = response + '\r\n' + 'Content-Type:text/html'
    response = response + '\r\n\r\n' + '<h1>400 Bad Request</h1>'
    return response
    
def HTTP_Bad_Cookie( request ) :
    response = request[0].split(' ')[2] + ' ' + STATUS401
    response = response + '\r\n' + 'Content-Type:text/html'
    response = response + '\r\n\r\n' + '<h1>Authenticating user failed.</h1>'
    response = response + '<h1>not in cookie SQL,request not allowed</h1>'
    return response

def HTTP_request_GET( request ) :
    path = request[0].split(' ')[1]
    reloc = False
    
    if path == '/' :
        path = "./index.html"
        
    elif( path == "/old_data.html" ) :
        path = "./relocate.html"
        reloc = True
        
    else :
        path = '.' + path
        
    version = request[0].split(' ')[2]
    cookies = None
        
    try :
        html_file = open(path, 'r')
        html_data = html_file.read()
        
        if version != "HTTP/1.1" :
            response = version + " " + STATUS505   
        elif reloc :
            response = version + " " + STATUS301
        else :
            response = version + " " + STATUS200
        
        index = 0
        for header in request :
            if index != 0 and index != 1 and len( header ) > 2 :
                if ( header.startswith('Cookie:') ) :
                    cookies = header.split(':')[1].strip()
                    response = response + '\r\n' + 'Set-Cookie:' + cookies
                    
                else :
                    response = response + '\r\n' + header # http header
            index += 1
        
        response = response + '\r\n' + 'Content-Disposition: attachment; filename=return.txt\r\n'
        if ( cookies == None ) :
            return HTTP_Bad_Cookie( request ) # no cookie
        
        else :
            response = response + '\r\n' + html_data
            print( "\n\n\n" + response + "\n\n\n" )
            return response
        
    except FileNotFoundError as e :
        html_file = open( './pageNotFound.html', 'r' ) # not found page
        html_data = html_file.read()
        response = request[0].split(' ')[2] + ' ' + STATUS404
        
        index = 0
        for header in request :
            if index != 0 and index != 1 :
                response = response + '\r\n' + header
            index += 1 
        response = response + '\r\n' + html_data
        print( "\n\n\n" + response + "\n\n\n" )
        return response
        
def HTTP_request_Post( request ) :
    path = request[0].split(' ')[1]
    if path == '/' :
        path = "./index.html"    
    else :
        path = '.' + path
        dir_path = path.replace( path.split('/')[-1], '' )
        
        # print( "post路徑 :" + dir_path )
        # print( "post檔案 :" + path.split('/')[-1] + '\n' )
        
        
        # 若路徑存在資料夾 且 資料夾不存在則建立資料夾
        if dir_path != "./" and ( not os.path.isdir(dir_path) ):
            os.makedirs( dir_path, mode=0o777 )
        
    version = request[0].split(' ')[2]
    cookies = None
        
    if ( version == "HTTP/1.1" ) :
        response = version + " " + STATUS200
        html_file = open(path, 'a')
        html_data = request[-1]
        html_file.write( html_data )
        html_file.close()
    else :
        response = version + " " + STATUS505
            
    index = 0
    for header in request[0:-1] :
        if index != 0 :
            if ( header.startswith('Cookie:') ) :
                cookies = header.split(':')[1].strip()
                response = response + '\r\n' + 'Set-Cookie:' + cookies
            
            else :
                response = response + '\r\n' + header
        index += 1
        
    if ( cookies == None ) :
        return HTTP_Bad_Cookie( request ) # no cookie
    else :
        response = response + '\r\n' + html_data
        
    print( "\n\n\n" + response + "\n\n\n" )
    return response
    
def HTTP_request_Head( request ) :
    path = request[0].split(' ')[1]
    if path == '/' :
        path = "./index.html"    
    else :
        path = '.' + path
        
    version = request[0].split(' ')[2]
    cookies = None
        
    try :
        html_file = open(path, 'r')
        
        if version == "HTTP/1.1" :
            response = version + " " + STATUS200
        else :
            response = version + " " + STATUS505
        
        index = 0
        for header in request[0:-1] :
            if index != 0 and index != 1 :
                if ( header.startswith('Cookie:') ) :
                    cookies = header.split(':')[1].strip()
                    response = response + '\r\n' + 'Set-Cookie:' + cookies
            
                else :
                    response = response + '\r\n' + header
            index += 1
        
        if ( cookies == None ) :
            return HTTP_Bad_Cookie( request ) # no cookie bad request
        else :
            response = response + '\r\n\r\n'
            return response
    
    except FileNotFoundError as e :
        response = request[0].split(' ')[2] + ' ' + STATUS404
        
        index = 0
        for header in request :
            if index != 0 and index != 1 :
                response = response + '\r\n' + header
            index += 1
        response = response + '\r\n\r\n'
        return response
    
def HTTP_request_Put( request ) :
    path = request[0].split(' ')[1]
    if path == '/' :
        path = "./index.html"    
    else :
        path = '.' + path
        dir_path = path.replace( path.split('/')[-1], '' )
        
        # print( "put路徑 :" + dir_path )
        # print( "put檔案 :" + path.split('/')[-1] + '\n' )
        
        # 若路徑存在資料夾 且 資料夾不存在則建立資料夾
        if dir_path != "./" and ( not os.path.isdir(dir_path) ):
            os.makedirs( dir_path, mode=0o777 )
        
    version = request[0].split(' ')[2]
    cookies = None
        
    if ( version == "HTTP/1.1" ) :
        response = version + " " + STATUS200
        html_file = open(path, 'w')
        html_data = request[-1]
        html_file.write( html_data )
        html_file.close()
    else :
        response = version + " " + STATUS505
        
    index = 0
    for header in request[0:-1] :
        if index != 0 :
            if ( header.startswith('Cookie:') ) :
                cookies = header.split(':')[1].strip()
                response = response + '\r\n' + 'Set-Cookie:' + cookies

            else :
                response = response + '\r\n' + header
        index += 1
        
    if ( cookies == None ) :
        return HTTP_Bad_Cookie( request ) # no cookie bad request
    else :
        response = response + '\r\n' + html_data
        print( "\n\n\n" + response + "\n\n\n" )
        return response
    
def HTTP_request_Delete( request ) :
    path = request[0].split(' ')[1]
    if path == '/' :
        path = "./index.html"    
    else :
        path = '.' + path
        
    version = request[0].split(' ')[2]
    cookies = None
        
    try :
        html_file = open(path, 'r')
        html_file.close()
        
        if version == "HTTP/1.1" :
            response = version + " " + STATUS200
        else :
            response = version + " " + STATUS505
        
        index = 0
        for header in request :
            if index != 0 and index != 1 :
                if ( header.startswith('Cookie:') ) :
                    cookies = header.split(':')[1].strip()
                    response = response + '\r\n' + 'Set-Cookie:' + cookies
            
                else :
                    response = response + '\r\n' + header
            index += 1
        
        if ( cookies == None ) :
            return HTTP_Bad_Cookie( request ) # no cookie bad request
        
        else :
            response = response + '\r\n\r\n'
            os.remove ( path )
            return response
    
    # 刪除不存在檔案error
    except FileNotFoundError as e :
        html_file = open( './pageNotFound.html', 'r' ) # not found page
        html_data = html_file.read()
        response = request[0].split(' ')[2] + ' ' + STATUS404
        
        index = 0
        for header in request :
            if index != 0 and index != 1 :
                response = response + '\r\n' + header
            index += 1 
        response = response + '\r\n' + html_data
        print( "\n\n\n" + response + "\n\n\n" )
        return response

def HTTP_request( request ) :
    
    if ( request[0].split(' ')[0] == 'GET' ) :
        return HTTP_request_GET( request )
    
    elif ( request[0].split(' ')[0] == 'POST' ) :
        request = HTML_list_merge( request )
        return HTTP_request_Post( request )
    
    elif ( request[0].split(' ')[0] == 'HEAD' ) :
        return HTTP_request_Head( request )
    
    elif ( request[0].split(' ')[0] == 'PUT' ) :
        request = HTML_list_merge( request )
        return HTTP_request_Put( request )
    
    elif ( request[0].split(' ')[0] == 'DELETE' ) :
        return HTTP_request_Delete( request )
    
    else :
        return HTTP_Bad_Request( request )

if __name__ == "__main__" :
    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    
    server.bind( ('127.0.0.1', 80) )
    server.listen(5)
    
    while True :
        client, addr = server.accept()
        http_request = client.recv(1024)
        http_request = http_request.decode()
        
        print( http_request )
        
        http_request = http_request.split('\r\n')
        response = HTTP_request( http_request )
        client.send( response.encode() )
        client.close()
        