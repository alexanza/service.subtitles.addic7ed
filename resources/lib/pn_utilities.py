# -*- coding: utf-8 -*- 

import sys
import os
import xmlrpclib
import unicodedata
import struct
from xml.dom import minidom
import urllib
import xbmc, xbmcvfs

try:
  # Python 2.6 +
  from hashlib import md5 as md5
  from hashlib import sha256
except ImportError:
  # Python 2.5 and earlier
  from md5 import md5
  from sha256 import sha256
  
__addon__      = sys.modules[ "__main__" ].__addon__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__version__    = sys.modules[ "__main__" ].__version__

USER_AGENT = "%s_v%s" % (__scriptname__.replace(" ","_"),__version__ )

LANGUAGES      = (

    # Full Language name[0]     podnapisi[1]  ISO 639-1[2]   ISO 639-1 Code[3]   Script Setting Language[4]   localized name id number[5]

    ("Albanian"                   , "29",       "sq",            "alb",                 "0",                     30201  ),
    ("Arabic"                     , "12",       "ar",            "ara",                 "1",                     30202  ),
    ("Belarusian"                 , "0" ,       "hy",            "arm",                 "2",                     30203  ),
    ("Bosnian"                    , "10",       "bs",            "bos",                 "3",                     30204  ),
    ("Bulgarian"                  , "33",       "bg",            "bul",                 "4",                     30205  ),
    ("Catalan"                    , "53",       "ca",            "cat",                 "5",                     30206  ),
    ("Chinese"                    , "17",       "zh",            "chi",                 "6",                     30207  ),
    ("Croatian"                   , "38",       "hr",            "hrv",                 "7",                     30208  ),
    ("Czech"                      , "7",        "cs",            "cze",                 "8",                     30209  ),
    ("Danish"                     , "24",       "da",            "dan",                 "9",                     30210  ),
    ("Dutch"                      , "23",       "nl",            "dut",                 "10",                    30211  ),
    ("English"                    , "2",        "en",            "eng",                 "11",                    30212  ),
    ("Estonian"                   , "20",       "et",            "est",                 "12",                    30213  ),
    ("Persian"                    , "52",       "fa",            "per",                 "13",                    30247  ),
    ("Finnish"                    , "31",       "fi",            "fin",                 "14",                    30214  ),
    ("French"                     , "8",        "fr",            "fre",                 "15",                    30215  ),
    ("German"                     , "5",        "de",            "ger",                 "16",                    30216  ),
    ("Greek"                      , "16",       "el",            "ell",                 "17",                    30217  ),
    ("Hebrew"                     , "22",       "he",            "heb",                 "18",                    30218  ),
    ("Hindi"                      , "42",       "hi",            "hin",                 "19",                    30219  ),
    ("Hungarian"                  , "15",       "hu",            "hun",                 "20",                    30220  ),
    ("Icelandic"                  , "6",        "is",            "ice",                 "21",                    30221  ),
    ("Indonesian"                 , "0",        "id",            "ind",                 "22",                    30222  ),
    ("Italian"                    , "9",        "it",            "ita",                 "23",                    30224  ),
    ("Japanese"                   , "11",       "ja",            "jpn",                 "24",                    30225  ),
    ("Korean"                     , "4",        "ko",            "kor",                 "25",                    30226  ),
    ("Latvian"                    , "21",       "lv",            "lav",                 "26",                    30227  ),
    ("Lithuanian"                 , "0",        "lt",            "lit",                 "27",                    30228  ),
    ("Macedonian"                 , "35",       "mk",            "mac",                 "28",                    30229  ),
    ("Malay"                      , "0",        "ms",            "may",                 "29",                    30248  ),    
    ("Norwegian"                  , "3",        "no",            "nor",                 "30",                    30230  ),
    ("Polish"                     , "26",       "pl",            "pol",                 "31",                    30232  ),
    ("Portuguese"                 , "32",       "pt",            "por",                 "32",                    30233  ),
    ("PortugueseBrazil"           , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Romanian"                   , "13",       "ro",            "rum",                 "34",                    30235  ),
    ("Russian"                    , "27",       "ru",            "rus",                 "35",                    30236  ),
    ("Serbian"                    , "36",       "sr",            "scc",                 "36",                    30237  ),
    ("Slovak"                     , "37",       "sk",            "slo",                 "37",                    30238  ),
    ("Slovenian"                  , "1",        "sl",            "slv",                 "38",                    30239  ),
    ("Spanish"                    , "28",       "es",            "spa",                 "39",                    30240  ),
    ("Swedish"                    , "25",       "sv",            "swe",                 "40",                    30242  ),
    ("Thai"                       , "0",        "th",            "tha",                 "41",                    30243  ),
    ("Turkish"                    , "30",       "tr",            "tur",                 "42",                    30244  ),
    ("Ukrainian"                  , "46",       "uk",            "ukr",                 "43",                    30245  ),
    ("Vietnamese"                 , "51",       "vi",            "vie",                 "44",                    30246  ),
    ("BosnianLatin"               , "10",       "bs",            "bos",                 "100",                   30204  ),
    ("Farsi"                      , "52",       "fa",            "per",                 "13",                    30247  ),
    ("English (US)"               , "2",        "en",            "eng",                 "100",                   30212  ),
    ("English (UK)"               , "2",        "en",            "eng",                 "100",                   30212  ),
    ("Portuguese (Brazilian)"     , "48",       "pt-br",         "pob",                 "100",                   30234  ),
    ("Portuguese (Brazil)"        , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Portuguese-BR"              , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Brazilian"                  , "48",       "pb",            "pob",                 "33",                    30234  ),
    ("Español (Latinoamérica)"    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Español (España)"           , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Spanish (Latin America)"    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Español"                    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("SerbianLatin"               , "36",       "sr",            "scc",                 "100",                   30237  ),
    ("Spanish (Spain)"            , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Chinese (Traditional)"      , "17",       "zh",            "chi",                 "100",                   30207  ),
    ("Chinese (Simplified)"       , "17",       "zh",            "chi",                 "100",                   30207  ) )


def languageTranslate(lang, lang_from, lang_to):
  for x in LANGUAGES:
    if lang == x[lang_from] :
      return x[lang_to]

def log(module, msg):
  xbmc.log((u"### [%s] - %s" % (module,msg,)).encode('utf-8'),level=xbmc.LOGDEBUG ) 

def compare_columns(b,a):
  return cmp( b["language_name"], a["language_name"] )  or cmp( a["sync"], b["sync"] ) 

def normalizeString(str):
  return unicodedata.normalize(
         'NFKD', unicode(unicode(str, 'utf-8'))
         ).encode('ascii','ignore')

def hashFile(file_path, rar=False):
    if rar:
      return OpensubtitlesHashRar(file_path)
      
    log( __name__,"Hash Standard file")  
    longlongformat = 'q'  # long long
    bytesize = struct.calcsize(longlongformat)
    f = xbmcvfs.File(file_path)
    
    filesize = f.size()
    hash = filesize
    
    if filesize < 65536 * 2:
        return "SizeError"
    
    buffer = f.read(65536)
    f.seek(max(0,filesize-65536),0)
    buffer += f.read(65536)
    f.close()
    for x in range((65536/bytesize)*2):
        size = x*bytesize
        (l_value,)= struct.unpack(longlongformat, buffer[size:size+bytesize])
        hash += l_value
        hash = hash & 0xFFFFFFFFFFFFFFFF
    
    returnHash = "%016x" % hash
    return filesize,returnHash

class OSDBServer:
  def create(self):
    self.subtitles_hash_list = []
    self.subtitles_list = []
    self.subtitles_name_list = []
 
  def mergesubtitles( self, stack ):
    if( len ( self.subtitles_hash_list ) > 0 ):
      for item in self.subtitles_hash_list:
        if item["format"].find( "srt" ) == 0 or item["format"].find( "sub" ) == 0:
          self.subtitles_list.append( item )

    if( len ( self.subtitles_name_list ) > 0 ):
      for item in self.subtitles_name_list:
        if item["format"].find( "srt" ) == 0 or item["format"].find( "sub" ) == 0:
          self.subtitles_list.append( item )                

    if( len ( self.subtitles_list ) > 0 ):
      self.subtitles_list = sorted(self.subtitles_list, compare_columns)

  def searchsubtitles_pod( self, movie_hash, lang , stack):
#    movie_hash = "e1b45885346cfa0b" # Matrix Hash, Debug only
    podserver = xmlrpclib.Server('http://ssp.podnapisi.net:8000')      
    pod_session = ""
    hash_pod =[str(movie_hash)]
    try:
      init = podserver.initiate(USER_AGENT)
      hash = md5()
      hash.update(__addon__.getSetting( "PNpass" ))
      password256 = sha256(str(hash.hexdigest()) + str(init['nonce'])).hexdigest()
      if str(init['status']) == "200":
        pod_session = init['session']
        podserver.authenticate(pod_session, __addon__.getSetting( "PNuser" ), password256)
        podserver.setFilters(pod_session, True, lang , False)
        search = podserver.search(pod_session , hash_pod)
        if str(search['status']) == "200" and len(search['results']) > 0 :
          search_item = search["results"][movie_hash]
          for item in search_item["subtitles"]:
            if item["lang"]:
              flag_image = item["lang"]
            else:                                                           
              flag_image = "-"
            link = str(item["id"])
            if item['release'] == "":
              episode = search_item["tvEpisode"]
              if str(episode) == "0":
                name = "%s (%s)" % (str(search_item["movieTitle"]),str(search_item["movieYear"]),)
              else:
                name = "%s S(%s)E(%s)" % (str(search_item["movieTitle"]),str(search_item["tvSeason"]), str(episode), )
            else:
              name = item['release']
            if item["inexact"]:
              sync1 = False
            else:
              sync1 = True
            
            self.subtitles_hash_list.append({'filename'      : name,
                                             'link'          : link,
                                             "language_name" : languageTranslate((item["lang"]),2,0),
                                             "language_flag" : flag_image,
                                             "language_id"   : item["lang"],
                                             "ID"            : item["id"],
                                             "sync"          : sync1,
                                             "format"        : "srt",
                                             "rating"        : str(int(item['rating'])*2),
                                             "hearing_imp"   : "n" in item['flags']
                                             })
        self.mergesubtitles(stack)
      return self.subtitles_list,pod_session
    except :
      return self.subtitles_list,pod_session

  def searchsubtitlesbyname_pod( self, name, tvshow, season, episode, lang, year, stack ):
    if len(tvshow) > 1:
      name = tvshow
    search_url=[]              
    search_url_base = "http://www.podnapisi.net/ppodnapisi/search?tbsl=1&sK=%s&sJ=%s&sY=%s&sTS=%s&sTE=%s&sXML=1&lang=0" % (name.replace(" ","+"), "%s", str(year), str(season), str(episode))
    
    subtitles = None
    
    for i in range(len(lang)):
      url = search_url_base % str(lang[i])
      log( __name__ ,"%s - Language %i" % (url,i))
      temp_subs = self.fetch(url)
      if temp_subs:
        if subtitles:
          subtitles = subtitles + temp_subs
        else:
          subtitles = temp_subs        
    try:
      if subtitles:
        url_base = "http://www.podnapisi.net/ppodnapisi/download/i/"
        for subtitle in subtitles:
          subtitle_id = 0
          rating      = 0
          filename    = ""
          movie       = ""
          lang_name   = ""
          lang_id     = ""
          flag_image  = ""
          link        = ""
          format      = "srt"
          hearing_imp = False
          if subtitle.getElementsByTagName("title")[0].firstChild:
            movie = subtitle.getElementsByTagName("title")[0].firstChild.data
          if subtitle.getElementsByTagName("release")[0].firstChild:
            filename = subtitle.getElementsByTagName("release")[0].firstChild.data
            if len(filename) < 2 :
              filename = "%s (%s).srt" % (movie,year,)
          else:
            filename = "%s (%s).srt" % (movie,year,) 
          if subtitle.getElementsByTagName("rating")[0].firstChild:
            rating = int(subtitle.getElementsByTagName("rating")[0].firstChild.data)*2
          if subtitle.getElementsByTagName("languageId")[0].firstChild:
            lang_name = languageTranslate(subtitle.getElementsByTagName("languageId")[0].firstChild.data, 1,2)
          if subtitle.getElementsByTagName("id")[0].firstChild:
            subtitle_id = subtitle.getElementsByTagName("id")[0].firstChild.data
          if subtitle.getElementsByTagName("flags")[0].firstChild:
              hearing_imp = "n" in subtitle.getElementsByTagName("flags")[0].firstChild.data
          flag_image = lang_name
          link = str(subtitle_id)
          self.subtitles_name_list.append({'filename':filename,
                                           'link':link,
                                           'language_name' : languageTranslate((lang_name),2,0),
                                           'language_id'   : lang_id,
                                           'language_flag' : flag_image,
                                           'movie'         : movie,
                                           "ID"            : subtitle_id,
                                           "rating"        : str(rating),
                                           "format"        : format,
                                           "sync"          : False,
                                           "hearing_imp"   : hearing_imp
                                           })
        self.mergesubtitles(stack)
      return self.subtitles_list
    except :
      return self.subtitles_list
  
  def download(self,pod_session,  id):
    podserver = xmlrpclib.Server('http://ssp.podnapisi.net:8000')  
    init = podserver.initiate(USER_AGENT)
    hash = md5()
    hash.update(__addon__.getSetting( "PNpass" ))
    id_pod =[]
    id_pod.append(str(id))
    password256 = sha256(str(hash.hexdigest()) + str(init['nonce'])).hexdigest()
    if str(init['status']) == "200":
      pod_session = init['session']
      auth = podserver.authenticate(pod_session, __addon__.getSetting( "PNuser" ), password256)
      if auth['status'] == 300: 
        log( __name__ ,"Authenticate [%s]" % "InvalidCredentials")
      download = podserver.download(pod_session , id_pod)
      if str(download['status']) == "200" and len(download['names']) > 0 :
        download_item = download["names"][0]
        if str(download["names"][0]['id']) == str(id):
          return "http://www.podnapisi.net/static/podnapisi/%s" % download["names"][0]['filename']
          
    return None  
  
  def fetch(self,url):
    socket = urllib.urlopen( url )
    result = socket.read()
    socket.close()
    xmldoc = minidom.parseString(result)
    return xmldoc.getElementsByTagName("subtitle")    
