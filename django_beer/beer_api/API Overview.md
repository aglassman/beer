Valid URIs
==========

URIs marked with DEEP ALLOWED can use ?deep=y GET parameter to return 1 layer of nested objects in the response.

Api Root /beer_api [GET,HEAD,OPTIONS]

The following URIs are accessible by:  

    Non-Authenticated users []  
	Authenticated users  [()]  
	Authenticated Admin users [({})]  
	
URI | METHOD | ORDER ALLOWED | DEEP ALLOWED
----|-----|:---------:|:-------:
/user_admin/ | [({GET,POST,HEAD,OPTIONS})]   | Y | 
/user_admin/{id}/ | [({GET, PUT, PATCH, DELETE, HEAD, OPTIONS})]   |  | 
/users/ |  [GET,HEAD,OPTIONS]  | Y |  
/users/{id}/ |  [GET,HEAD,OPTIONS]   |  | Y
/styles/ |  [GET,HEAD,OPTIONS,(POST)]   | Y | 
/styles/{id}/ |  [GET, HEAD, OPTIONS, (PUT, PATCH, DELETE)]   |  | Y
/glass_types/  | [GET,HEAD,OPTIONS,(POST)]   | Y | 
/glass_types/{id}/ |  [GET, HEAD, OPTIONS, (PUT, PATCH, DELETE)]   |  | 
/breweries/ |  [GET,HEAD,OPTIONS,(POST)] | Y | 
/breweries/{id}/ |  [GET, HEAD, OPTIONS, (PUT, PATCH, DELETE)] |  | 
/beers/ |  [GET,HEAD,OPTIONS,(POST)] | Y | 
/beers/{id}/ |  [GET, HEAD, OPTIONS, (PUT, PATCH, DELETE)]  |  | Y
/beer_reviews/  | [GET,HEAD,OPTIONS,(POST)] | Y | 
/beer_reviews/{id}/ |  [GET, HEAD, OPTIONS, (PUT, PATCH, DELETE)]   |  | Y
/favorites/ |  [GET,HEAD,OPTIONS,(POST)] | Y | 
/favorites/{id}/  | [GET, HEAD, OPTIONS, (PUT, PATCH, DELETE)]  |  | Y
/user_list/favorites/{id}/ |  [GET,HEAD,OPTIONS] | Y |   
/user_list/beer_contributions/{id}/ |  [GET,HEAD,OPTIONS] | Y |  
/user_list/beer_reviews/{id}/ |  [GET,HEAD,OPTIONS]  | Y | 
/beer_list/reviews/{id}/ |  [GET,HEAD,OPTIONS]  | Y | 
/beer_list/overall/{id}/ |  [GET,HEAD,OPTIONS]  |  | Y 
/beer_list/favorited_by/{id}/ |  [GET,HEAD,OPTIONS]  | Y | 

Ordering
========
Any GET request that returns a list can be ordered using get parameters.

For example, to order users by username:

http://example.com/api/users?ordering=username

The client may also specify reverse orderings by prefixing the field name with '-', like so:

http://example.com/api/users?ordering=-username

Multiple orderings may also be specified:

http://example.com/api/users?ordering=account,username

Data Format
===========

Examples of json data for post

    Style
	{
	    "style": "", 
	    "description": ""
	}

    Glass Type
	{
	    "glass_type": "", 
	    "description": ""
	}

    Brewery
	{
	    "name": "", 
	    "brewery_location": ""
	}

    Beer
	{
	    "added_by_user": null, 
	    "name": "", 
	    "ibu": 0, 
	    "calories": 0, 
	    "abv": "0", 
	    "brewery": null, 
	    "style": null, 
	    "glass_type": null, 
	    "description": ""
	}

    Beer Review
	{
	    "user": null, 
	    "beer": null, 
	    "aroma": 0, 
	    "appearance": 0, 
	    "taste": 0, 
	    "palate": 0, 
	    "bottle_style": 0, 
	    "comments": ""
	}

    User
	{
	    "username": "", 
	    "email": "", 
	    "password": "", 
	    "is_staff": false, 
	    "is_active": false
	}

    Favorite
	{
	    "user": 2, 
	    "beer": 8
	}

USER AUTHENTICATED POSTS
========================
Posts that set the user field should be set to null.  This will be overwritten with the currently authenticated user.  This is true for the following URIs

/beers/  
/beer_reviews/  
/favorites/  