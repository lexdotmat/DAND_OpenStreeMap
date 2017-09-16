# OpenStreetMap Data Case Study

### Map Area
Basel, Switzerland 

- [https://www.openstreetmap.org/relation/1683619](https://www.openstreetmap.org/relation/1683619)


This city is the city where I'm currently living, Basel, I like to use this project as an opportunity to discover the city as well as the OpenStreetMap.org website. 


## Problems Encountered in the Map

After initially downloading a small sample size of the Basel area and running it against a provisional data.py file, I noticed one main problems with the data, which is the phone number format. 

The following paragraph will describes the auditing and cleaning process applied to this particular field. 

Another data quality problem is the country value, in most of the case the 2 digit country code is used, however, in some cases the full name i.e. "Switzerland" is being used.

In order to harmonized this, a function has been designed to take care of the cases where the name is written in full.
### phone formatting


The audit of the phone format has been run on a partial file with this function that report in the same time the dictionnary content:

```python
phone_format = {}
def audit_phone_type(Phone_number):

    # phone number format: +41 or 0 xx xxx xx xx
    # to finish

    formatphone = Phone_number.translate(mapping)
    if formatphone not in phone_format:
        phone_format[formatphone] = 1
    else:
        phone_format[formatphone] += 1

    print phone_format
    return phone_cleaning(Phone_number)
 ```  

Here are the results for the phone format: 
 
```python
{'+xx xx xxxxxxx': 2,
 'xxx xxx xx xx/xx': 1,
 'xxx xxx xx xx': 1,
 '+xx(x)xxxxxxxxx': 1,
 '+xx xx xxx xx xx': 7,
 '+xx xx xxx xxxx': 1,
 '+xxxxxxxxxxx': 1,
 '+xxxxxxx xx xx': 1,
 'xxxxxxxxxx': 1}
```
We can see that the Swiss format (+xx xx xxx xx xx ) is the most used (7 occurrences found) and that needs to be harmonized.

In order to clean the phone number, the following function is used: 

```python 
def phone_cleaning(phone_raw):
    '''
    :param phone_raw: a swiss phone number raw number in either format.
    :return: the phone number in the format +41 xx xxx xx xx
    '''
    phone_raw.replace(" ", "")
    return "+41"+ " " +phone_raw[-9:-7] + " " + phone_raw[-7:-4] + " " + phone_raw[-4:-2] + " " + phone_raw[-2:]
```

once the format used, the following SQL query is used to consult the content of the db:
```sql
select * from nodes_tags where key = "phone";
```

```sql
364938305|phone|+41 61 272 11 52|regular
364939823|phone|+41 61 2713933|regular
366084122|phone|+41 61 560 85 85|contact
366084122|phone|+41 61 560 8585|regular
569316805|phone|+41 61 2758000|regular
569316914|phone|+41 61 205 85 50|contact
606129885|phone|+41 61 361 73 09|regular
1145999573|phone|+41 848 888 888|contact
1197413430|phone|+4161361 02 12|regular
1255857521|phone|061 363 00 00|regular
```
The query after the cleaning, note that only the 'regular' tags have been corrected due to the audit of only this type of tags.
```sql
364938305|phone|+41 61 272 11 52|regular
364939823|phone|+41 61 271 39 33|regular
366084122|phone|+41 61 560 85 85|contact
366084122|phone|+41 61 560 85 85|regular
569316805|phone|+41 61 275 80 00|regular
569316914|phone|+41 61 205 85 50|contact
606129885|phone|+41 61 361 73 09|regular
1145999573|phone|+41 848 888 888|contact
```

Note that the Data.py file has been updated with the auditing and cleaning code (without print function, in order to make the process faster)
## Country codes and names

After looking at the data, I found some very odd cases, the area is in Switzerland and, when querying the keys "country",
I received the following values:

```sql
sqlite> select value, count(*) from nodes_tags where key = 'country' group by value;
```

```sql
CH|1318
DE|2
PH|2
Switzerland|4
```

The result was very interesting, especially for the PH, at first, I thougth it was a mistake from CH but I queryied the sql database and found the following:

```sql
sqlite> select * from nodes_tags where value = 'PH' group by value;
569316909|country|PH|regular
```

```sql
sqlite> select * from nodes_tags where id  = '569316909' group by value;
569316909|country|PH|regular
569316909|name|Philippinisches Konsulat|regular
569316909|amenity|embassy|regular
```

The country field has been used for a Consulat! 

it was the same for the DE tag:
```sql
3849747906|target|CH|regular
3849747906|country|DE|regular
3849747906|name|Honorarkonsul der Bundesrepublik Deutschland Basel|regular
3849747906|amenity|embassy|regular
3849747906|website|https://www.deutscher-honorarkonsul-basel.ch/|regular
```

The decision has been taken just to take care about the Switzerland tag. 


# Data Overview and Additional Ideas
This section contains basic statistics about the dataset, the MongoDB queries used to gather them, and some additional ideas about the data in context.

### File sizes
```
basel.osm ......... 60.6 MB
OS_Basel_FULL.db .......... 32.6 MB
nodes.csv ............. 18.8 MB
nodes_tags.csv ........ 3.1 MB
ways.csv .............. 2 MB
ways_tags.csv ......... 3.4 MB
ways_nodes.cv ......... 7.6 MB  
```  

### Number of nodes
```
sqlite> SELECT COUNT(*) FROM nodes;
```
235839

### Number of ways
```
sqlite> SELECT COUNT(*) FROM ways;
```
34900

### Number of unique users
```sql
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
```
897

### Top 10 contributing users
```sql
sqlite> SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;
```

```sql
stibe|104851
oscarrazu|56236
calubi|24973
Geb_imp|7150
kaiD|5238
MischaF|4748
roki|4447
Nzara|4325
mdk|4250
soemisch|3427
```

The Basel Wiki OSM highlight that Stibe is the user who developped the import algorithm in February 2014

http://wiki.openstreetmap.org/wiki/DE:Switzerland:Basel-Stadt



### Number of users appearing only once (having 1 post)
```sql
sqlite> SELECT COUNT(*) 
FROM
    (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num=1)  u;
```
180

# Additional Ideas

## Contributor statistics and gamification suggestion 
The contributions of users seems incredibly skewed, possibly due to automated versus manual map editing (the word “bot” appears in some usernames). Here are some user percentage statistics:

This is confirmed by the OSM WIKI on the Basel Area. Among the top ten users, 
- Top user contribution percentage (“stibe”) 48%
- Combined top 2 users' contribution (“Stibe” and “carrazu”) 73%


Thinking about these user percentages, I’m reminded of “gamification” as a motivating force for contribution. In the context of the OpenStreetMap, if user data were more prominently displayed, perhaps others would take an initiative in submitting more edits to the map. And, if everyone sees that only a handful of power users are creating more than 90% a of given map, that might spur the creation of more efficient bots, especially if certain gamification elements were present, such as rewards, badges, or a leaderboard. 

## Additional Data Exploration

### Top 10 appearing amenities

```sql
sqlite> SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```

```sql
bench|416
restaurant|233
vending_machine|167
cafe|63
post_box|63
parking|58
recycling|57
waste_basket|54
toilets|52
atm|50
```

### Biggest religion 

```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 1;
```
```sql
christian|8
```

### Most popular cuisines

```sql
select value, count(value) 
from nodes_tags WHERE key  = 'cuisine'
group by value order by count(value) desc limit 10;
```

```sql
italian|20
regional|19
pizza|11
coffee_shop|10
burger|7
turkish|6
kebab|5
asian|4
japanese|3
chinese|2
```

### Most Popular Shop type

```sql
select value, count(value) 
from nodes_tags where key = "shop" 
group by value 
order by count(value) desc
limit 15;
```

```sql
supermarket|80
convenience|32
hairdresser|27
kiosk|24
bakery|21
bicycle|19
clothes|14
florist|14
books|12
confectionery|8
hifi|7
yes|7
optician|6
toys|6
jewelry|5
```

# Conclusion

After this review of the data it’s obvious that the Basel area is incomplete, though I believe it has been already very well cleaned and seems to be connected with the local Geo data from the official Basel city organization (http://www.stadtplan.bs.ch/geoviewer/)
 
It interests me to notice a fair amount of GPS data makes it into OpenStreetMap.org on account of users’ efforts, whether by scripting a map editing bot or otherwise. With a rough GPS data processor in place and working together with a more robust data processor similar to data.pyI think it would be possible to input a great amount of cleaned data to OpenStreetMap.org.
