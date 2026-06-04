import math
import random
from dataclasses import dataclass
from typing import Dict, List

import streamlit as st

st.set_page_config(page_title="Football Draft MVP", page_icon="⚽", layout="wide")

SLOT_DEFS = [
    {"id": "GK", "label": "GK", "group": "GK"},
    {"id": "CB1", "label": "CB", "group": "CB"},
    {"id": "CB2", "label": "CB", "group": "CB"},
    {"id": "FB1", "label": "LB/RB", "group": "FB"},
    {"id": "FB2", "label": "LB/RB", "group": "FB"},
    {"id": "CM1", "label": "CM", "group": "CM"},
    {"id": "CM2", "label": "CM", "group": "CM"},
    {"id": "CM3", "label": "CM", "group": "CM"},
    {"id": "LW", "label": "LW", "group": "LW"},
    {"id": "RW", "label": "RW", "group": "RW"},
    {"id": "ST", "label": "ST", "group": "ST"},
]

TEAMS = [
    {"id": "manchester_united_1999", "league": "Premier League", "name": "Manchester United", "era": "1999 Treble", "score": 95},
    {"id": "arsenal_2004", "league": "Premier League", "name": "Arsenal", "era": "2004 Invincibles", "score": 93},
    {"id": "chelsea_2005", "league": "Premier League", "name": "Chelsea", "era": "2004-05 Mourinho", "score": 91},
    {"id": "manchester_city_2018", "league": "Premier League", "name": "Manchester City", "era": "2018 Centurions", "score": 94},
    {"id": "manchester_city_2023", "league": "Premier League", "name": "Manchester City", "era": "2022-23 Treble", "score": 96},
    {"id": "liverpool_2019", "league": "Premier League", "name": "Liverpool", "era": "2019 Champions League winners", "score": 93},
    {"id": "liverpool_2020", "league": "Premier League", "name": "Liverpool", "era": "2019-20 Premier League champions", "score": 94},

    {"id": "barcelona_2009", "league": "La Liga", "name": "Barcelona", "era": "2008-09 Guardiola", "score": 95},
    {"id": "barcelona_2011", "league": "La Liga", "name": "Barcelona", "era": "2010-11 Guardiola", "score": 97},
    {"id": "barcelona_2015", "league": "La Liga", "name": "Barcelona", "era": "2014-15 MSN", "score": 96},
    {"id": "real_madrid_2002", "league": "La Liga", "name": "Real Madrid", "era": "2001-02 Galacticos", "score": 92},
    {"id": "real_madrid_2017", "league": "La Liga", "name": "Real Madrid", "era": "2016-17 Three-peat", "score": 96},
    {"id": "real_madrid_2024", "league": "La Liga", "name": "Real Madrid", "era": "2023-24 Champions League winners", "score": 97},
    {"id": "atletico_madrid_2014", "league": "La Liga", "name": "Atletico Madrid", "era": "2013-14 champions", "score": 90},

    {"id": "ac_milan_1994", "league": "Serie A", "name": "AC Milan", "era": "1993-94", "score": 95},
    {"id": "ac_milan_2007", "league": "Serie A", "name": "AC Milan", "era": "2006-07 Champions League winners", "score": 92},
    {"id": "inter_2010", "league": "Serie A", "name": "Inter Milan", "era": "2009-10 Treble", "score": 94},
    {"id": "juventus_1997", "league": "Serie A", "name": "Juventus", "era": "1996-97", "score": 90},
    {"id": "juventus_2015", "league": "Serie A", "name": "Juventus", "era": "2014-15 finalists", "score": 91},
    {"id": "napoli_2023", "league": "Serie A", "name": "Napoli", "era": "2022-23 champions", "score": 88},
    {"id": "roma_2001", "league": "Serie A", "name": "Roma", "era": "2000-01 champions", "score": 87},

    {"id": "bayern_2013", "league": "Bundesliga", "name": "Bayern Munich", "era": "2012-13 Treble", "score": 95},
    {"id": "bayern_2020", "league": "Bundesliga", "name": "Bayern Munich", "era": "2019-20 Sextuple", "score": 97},
    {"id": "dortmund_2013", "league": "Bundesliga", "name": "Borussia Dortmund", "era": "2012-13 finalists", "score": 90},
    {"id": "leverkusen_2024", "league": "Bundesliga", "name": "Bayer Leverkusen", "era": "2023-24 Invincibles", "score": 94},
    {"id": "psg_2016", "league": "Ligue 1", "name": "Paris Saint-Germain", "era": "2015-16", "score": 90},
    {"id": "psg_2025", "league": "Ligue 1", "name": "Paris Saint-Germain", "era": "2024-25 champions", "score": 95},
    {"id": "monaco_2017", "league": "Ligue 1", "name": "Monaco", "era": "2016-17 Mbappe era", "score": 91},

    {"id": "galatasaray_legends", "league": "Turkey", "name": "Galatasaray", "era": "Legends", "score": 92},
    {"id": "fenerbahce_legends", "league": "Turkey", "name": "Fenerbahce", "era": "Legends", "score": 91},
    {"id": "besiktas_legends", "league": "Turkey", "name": "Besiktas", "era": "Legends", "score": 90},
    {"id": "belgium_golden_generation", "league": "International", "name": "Belgium", "era": "Golden Generation", "score": 93},
]

TEAM_PLAYERS: Dict[str, List[Dict[str, str]]] = {
    "manchester_united_1999": [
        {"name": "Peter Schmeichel", "position": "GK"},
        {"name": "Gary Neville", "position": "RB"},
        {"name": "Jaap Stam", "position": "CB"},
        {"name": "Ronny Johnsen", "position": "CB"},
        {"name": "Denis Irwin", "position": "LB"},
        {"name": "Roy Keane", "position": "CM"},
        {"name": "Paul Scholes", "position": "CM"},
        {"name": "David Beckham", "position": "RW"},
        {"name": "Ryan Giggs", "position": "LW"},
        {"name": "Dwight Yorke", "position": "ST"},
        {"name": "Andy Cole", "position": "ST"},
    ],
    "arsenal_2004": [
        {"name": "Jens Lehmann", "position": "GK"},
        {"name": "Lauren", "position": "RB"},
        {"name": "Sol Campbell", "position": "CB"},
        {"name": "Kolo Toure", "position": "CB"},
        {"name": "Ashley Cole", "position": "LB"},
        {"name": "Patrick Vieira", "position": "CM"},
        {"name": "Gilberto Silva", "position": "CM"},
        {"name": "Robert Pires", "position": "LW"},
        {"name": "Freddie Ljungberg", "position": "RW"},
        {"name": "Dennis Bergkamp", "position": "ST"},
        {"name": "Thierry Henry", "position": "ST"},
    ],
    "chelsea_2005": [
        {"name": "Petr Cech", "position": "GK"},
        {"name": "Paulo Ferreira", "position": "RB"},
        {"name": "John Terry", "position": "CB"},
        {"name": "Ricardo Carvalho", "position": "CB"},
        {"name": "William Gallas", "position": "LB"},
        {"name": "Claude Makelele", "position": "CM"},
        {"name": "Frank Lampard", "position": "CM"},
        {"name": "Arjen Robben", "position": "RW"},
        {"name": "Damien Duff", "position": "LW"},
        {"name": "Joe Cole", "position": "ST"},
        {"name": "Didier Drogba", "position": "ST"},
    ],
    "manchester_city_2018": [
        {"name": "Ederson", "position": "GK"},
        {"name": "Kyle Walker", "position": "RB"},
        {"name": "Vincent Kompany", "position": "CB"},
        {"name": "Nicolas Otamendi", "position": "CB"},
        {"name": "Fabian Delph", "position": "LB"},
        {"name": "Fernandinho", "position": "CM"},
        {"name": "David Silva", "position": "CM"},
        {"name": "Kevin De Bruyne", "position": "CM"},
        {"name": "Raheem Sterling", "position": "RW"},
        {"name": "Leroy Sane", "position": "LW"},
        {"name": "Sergio Aguero", "position": "ST"},
    ],
    "manchester_city_2023": [
        {"name": "Ederson", "position": "GK"},
        {"name": "Kyle Walker", "position": "RB"},
        {"name": "Ruben Dias", "position": "CB"},
        {"name": "John Stones", "position": "CB"},
        {"name": "Nathan Ake", "position": "LB"},
        {"name": "Rodri", "position": "CM"},
        {"name": "Kevin De Bruyne", "position": "CM"},
        {"name": "Bernardo Silva", "position": "CM"},
        {"name": "Jack Grealish", "position": "LW"},
        {"name": "Julian Alvarez", "position": "RW"},
        {"name": "Erling Haaland", "position": "ST"},
    ],
    "liverpool_2019": [
        {"name": "Alisson", "position": "GK"},
        {"name": "Trent Alexander-Arnold", "position": "RB"},
        {"name": "Virgil van Dijk", "position": "CB"},
        {"name": "Joel Matip", "position": "CB"},
        {"name": "Andrew Robertson", "position": "LB"},
        {"name": "Fabinho", "position": "CM"},
        {"name": "Jordan Henderson", "position": "CM"},
        {"name": "Georginio Wijnaldum", "position": "CM"},
        {"name": "Mohamed Salah", "position": "RW"},
        {"name": "Sadio Mane", "position": "LW"},
        {"name": "Roberto Firmino", "position": "ST"},
    ],
    "liverpool_2020": [
        {"name": "Alisson", "position": "GK"},
        {"name": "Trent Alexander-Arnold", "position": "RB"},
        {"name": "Virgil van Dijk", "position": "CB"},
        {"name": "Joe Gomez", "position": "CB"},
        {"name": "Andrew Robertson", "position": "LB"},
        {"name": "Fabinho", "position": "CM"},
        {"name": "Jordan Henderson", "position": "CM"},
        {"name": "Georginio Wijnaldum", "position": "CM"},
        {"name": "Mohamed Salah", "position": "RW"},
        {"name": "Sadio Mane", "position": "LW"},
        {"name": "Roberto Firmino", "position": "ST"},
    ],
    "barcelona_2009": [
        {"name": "Victor Valdes", "position": "GK"},
        {"name": "Dani Alves", "position": "RB"},
        {"name": "Gerard Pique", "position": "CB"},
        {"name": "Carles Puyol", "position": "CB"},
        {"name": "Eric Abidal", "position": "LB"},
        {"name": "Sergio Busquets", "position": "CM"},
        {"name": "Xavi", "position": "CM"},
        {"name": "Andres Iniesta", "position": "CM"},
        {"name": "Lionel Messi", "position": "RW"},
        {"name": "Samuel Eto'o", "position": "ST"},
        {"name": "Thierry Henry", "position": "LW"},
    ],
    "barcelona_2011": [
        {"name": "Victor Valdes", "position": "GK"},
        {"name": "Dani Alves", "position": "RB"},
        {"name": "Gerard Pique", "position": "CB"},
        {"name": "Carles Puyol", "position": "CB"},
        {"name": "Eric Abidal", "position": "LB"},
        {"name": "Sergio Busquets", "position": "CM"},
        {"name": "Xavi", "position": "CM"},
        {"name": "Andres Iniesta", "position": "CM"},
        {"name": "Lionel Messi", "position": "RW"},
        {"name": "David Villa", "position": "ST"},
        {"name": "Pedro", "position": "LW"},
    ],
    "barcelona_2015": [
        {"name": "Marc-Andre ter Stegen", "position": "GK"},
        {"name": "Dani Alves", "position": "RB"},
        {"name": "Gerard Pique", "position": "CB"},
        {"name": "Javier Mascherano", "position": "CB"},
        {"name": "Jordi Alba", "position": "LB"},
        {"name": "Sergio Busquets", "position": "CM"},
        {"name": "Andres Iniesta", "position": "CM"},
        {"name": "Ivan Rakitic", "position": "CM"},
        {"name": "Lionel Messi", "position": "RW"},
        {"name": "Luis Suarez", "position": "ST"},
        {"name": "Neymar", "position": "LW"},
    ],
    "real_madrid_2002": [
        {"name": "Iker Casillas", "position": "GK"},
        {"name": "Michel Salgado", "position": "RB"},
        {"name": "Fernando Hierro", "position": "CB"},
        {"name": "Claude Makelele", "position": "CM"},
        {"name": "Roberto Carlos", "position": "LB"},
        {"name": "Zinedine Zidane", "position": "CM"},
        {"name": "Luis Figo", "position": "RW"},
        {"name": "Raul", "position": "ST"},
        {"name": "Ronaldo Nazario", "position": "ST"},
        {"name": "Guti", "position": "CM"},
        {"name": "Steve McManaman", "position": "LW"},
    ],
    "real_madrid_2017": [
        {"name": "Keylor Navas", "position": "GK"},
        {"name": "Dani Carvajal", "position": "RB"},
        {"name": "Sergio Ramos", "position": "CB"},
        {"name": "Raphael Varane", "position": "CB"},
        {"name": "Marcelo", "position": "LB"},
        {"name": "Casemiro", "position": "CM"},
        {"name": "Luka Modric", "position": "CM"},
        {"name": "Toni Kroos", "position": "CM"},
        {"name": "Cristiano Ronaldo", "position": "LW"},
        {"name": "Karim Benzema", "position": "ST"},
        {"name": "Gareth Bale", "position": "RW"},
    ],
    "real_madrid_2024": [
        {"name": "Andriy Lunin", "position": "GK"},
        {"name": "Dani Carvajal", "position": "RB"},
        {"name": "Antonio Rudiger", "position": "CB"},
        {"name": "Nacho", "position": "CB"},
        {"name": "Ferland Mendy", "position": "LB"},
        {"name": "Federico Valverde", "position": "CM"},
        {"name": "Aurelien Tchouameni", "position": "CM"},
        {"name": "Jude Bellingham", "position": "CM"},
        {"name": "Vinicius Junior", "position": "LW"},
        {"name": "Rodrygo", "position": "RW"},
        {"name": "Toni Kroos", "position": "CM"},
    ],
    "atletico_madrid_2014": [
        {"name": "Thibaut Courtois", "position": "GK"},
        {"name": "Juanfran", "position": "RB"},
        {"name": "Diego Godin", "position": "CB"},
        {"name": "Miranda", "position": "CB"},
        {"name": "Filipe Luis", "position": "LB"},
        {"name": "Gabi", "position": "CM"},
        {"name": "Koke", "position": "CM"},
        {"name": "Arda Turan", "position": "RW"},
        {"name": "Raul Garcia", "position": "CM"},
        {"name": "Diego Costa", "position": "ST"},
        {"name": "David Villa", "position": "LW"},
    ],
    "ac_milan_1994": [
        {"name": "Sebastiano Rossi", "position": "GK"},
        {"name": "Mauro Tassotti", "position": "RB"},
        {"name": "Franco Baresi", "position": "CB"},
        {"name": "Alessandro Costacurta", "position": "CB"},
        {"name": "Paolo Maldini", "position": "LB"},
        {"name": "Marcel Desailly", "position": "CM"},
        {"name": "Demetrio Albertini", "position": "CM"},
        {"name": "Zvonimir Boban", "position": "CM"},
        {"name": "Dejan Savicevic", "position": "RW"},
        {"name": "Daniele Massaro", "position": "ST"},
        {"name": "Jean-Pierre Papin", "position": "ST"},
    ],
    "ac_milan_2007": [
        {"name": "Dida", "position": "GK"},
        {"name": "Cafu", "position": "RB"},
        {"name": "Alessandro Nesta", "position": "CB"},
        {"name": "Paolo Maldini", "position": "CB"},
        {"name": "Massimo Oddo", "position": "LB"},
        {"name": "Gennaro Gattuso", "position": "CM"},
        {"name": "Andrea Pirlo", "position": "CM"},
        {"name": "Clarence Seedorf", "position": "CM"},
        {"name": "Kaka", "position": "RW"},
        {"name": "Filippo Inzaghi", "position": "ST"},
        {"name": "Alberto Gilardino", "position": "ST"},
    ],
    "inter_2010": [
        {"name": "Julio Cesar", "position": "GK"},
        {"name": "Maicon", "position": "RB"},
        {"name": "Lucio", "position": "CB"},
        {"name": "Walter Samuel", "position": "CB"},
        {"name": "Javier Zanetti", "position": "LB"},
        {"name": "Esteban Cambiasso", "position": "CM"},
        {"name": "Wesley Sneijder", "position": "CM"},
        {"name": "Goran Pandev", "position": "LW"},
        {"name": "Samuel Eto'o", "position": "RW"},
        {"name": "Diego Milito", "position": "ST"},
        {"name": "Thiago Motta", "position": "CM"},
    ],
    "juventus_1997": [
        {"name": "Angelo Peruzzi", "position": "GK"},
        {"name": "Ciro Ferrara", "position": "CB"},
        {"name": "Paolo Montero", "position": "CB"},
        {"name": "Mark Iuliano", "position": "CB"},
        {"name": "Antonio Conte", "position": "CM"},
        {"name": "Didier Deschamps", "position": "CM"},
        {"name": "Zinedine Zidane", "position": "CM"},
        {"name": "Alessandro Del Piero", "position": "ST"},
        {"name": "Christian Vieri", "position": "ST"},
        {"name": "Alen Boksic", "position": "ST"},
        {"name": "Vladimir Jugovic", "position": "CM"},
    ],
    "juventus_2015": [
        {"name": "Gianluigi Buffon", "position": "GK"},
        {"name": "Stephan Lichtsteiner", "position": "RB"},
        {"name": "Leonardo Bonucci", "position": "CB"},
        {"name": "Giorgio Chiellini", "position": "CB"},
        {"name": "Patrice Evra", "position": "LB"},
        {"name": "Andrea Pirlo", "position": "CM"},
        {"name": "Paul Pogba", "position": "CM"},
        {"name": "Arturo Vidal", "position": "CM"},
        {"name": "Claudio Marchisio", "position": "CM"},
        {"name": "Carlos Tevez", "position": "ST"},
        {"name": "Alvaro Morata", "position": "ST"},
    ],
    "napoli_2023": [
        {"name": "Alex Meret", "position": "GK"},
        {"name": "Giovanni Di Lorenzo", "position": "RB"},
        {"name": "Kim Min-jae", "position": "CB"},
        {"name": "Amir Rrahmani", "position": "CB"},
        {"name": "Mario Rui", "position": "LB"},
        {"name": "Stanislav Lobotka", "position": "CM"},
        {"name": "Andre-Frank Zambo Anguissa", "position": "CM"},
        {"name": "Piotr Zielinski", "position": "CM"},
        {"name": "Khvicha Kvaratskhelia", "position": "LW"},
        {"name": "Victor Osimhen", "position": "ST"},
        {"name": "Hirving Lozano", "position": "RW"},
    ],
    "roma_2001": [
        {"name": "Francesco Antonioli", "position": "GK"},
        {"name": "Cafu", "position": "RB"},
        {"name": "Walter Samuel", "position": "CB"},
        {"name": "Aldair", "position": "CB"},
        {"name": "Vincent Candela", "position": "LB"},
        {"name": "Emerson", "position": "CM"},
        {"name": "Damiano Tommasi", "position": "CM"},
        {"name": "Cristian Panucci", "position": "RB"},
        {"name": "Francesco Totti", "position": "ST"},
        {"name": "Gabriel Batistuta", "position": "ST"},
        {"name": "Vincenzo Montella", "position": "ST"},
    ],
    "bayern_2013": [
        {"name": "Manuel Neuer", "position": "GK"},
        {"name": "Philipp Lahm", "position": "RB"},
        {"name": "Jerome Boateng", "position": "CB"},
        {"name": "Dante", "position": "CB"},
        {"name": "David Alaba", "position": "LB"},
        {"name": "Bastian Schweinsteiger", "position": "CM"},
        {"name": "Javi Martinez", "position": "CM"},
        {"name": "Thomas Muller", "position": "CM"},
        {"name": "Franck Ribery", "position": "LW"},
        {"name": "Arjen Robben", "position": "RW"},
        {"name": "Mario Mandzukic", "position": "ST"},
    ],
    "bayern_2020": [
        {"name": "Manuel Neuer", "position": "GK"},
        {"name": "Joshua Kimmich", "position": "RB"},
        {"name": "Jerome Boateng", "position": "CB"},
        {"name": "David Alaba", "position": "CB"},
        {"name": "Alphonso Davies", "position": "LB"},
        {"name": "Leon Goretzka", "position": "CM"},
        {"name": "Thiago Alcantara", "position": "CM"},
        {"name": "Thomas Muller", "position": "CM"},
        {"name": "Serge Gnabry", "position": "RW"},
        {"name": "Kingsley Coman", "position": "LW"},
        {"name": "Robert Lewandowski", "position": "ST"},
    ],
    "dortmund_2013": [
        {"name": "Roman Weidenfeller", "position": "GK"},
        {"name": "Lukasz Piszczek", "position": "RB"},
        {"name": "Mats Hummels", "position": "CB"},
        {"name": "Neven Subotic", "position": "CB"},
        {"name": "Marcel Schmelzer", "position": "LB"},
        {"name": "Ilkay Gundogan", "position": "CM"},
        {"name": "Sven Bender", "position": "CM"},
        {"name": "Marco Reus", "position": "LW"},
        {"name": "Mario Gotze", "position": "RW"},
        {"name": "Robert Lewandowski", "position": "ST"},
        {"name": "Jakub Blaszczykowski", "position": "RW"},
    ],
    "leverkusen_2024": [
        {"name": "Lukas Hradecky", "position": "GK"},
        {"name": "Jeremie Frimpong", "position": "RB"},
        {"name": "Jonathan Tah", "position": "CB"},
        {"name": "Edmond Tapsoba", "position": "CB"},
        {"name": "Piero Hincapie", "position": "LB"},
        {"name": "Granit Xhaka", "position": "CM"},
        {"name": "Exequiel Palacios", "position": "CM"},
        {"name": "Florian Wirtz", "position": "CM"},
        {"name": "Alejandro Grimaldo", "position": "LB"},
        {"name": "Victor Boniface", "position": "ST"},
        {"name": "Patrik Schick", "position": "ST"},
    ],
    "psg_2016": [
        {"name": "Kevin Trapp", "position": "GK"},
        {"name": "Serge Aurier", "position": "RB"},
        {"name": "Thiago Silva", "position": "CB"},
        {"name": "David Luiz", "position": "CB"},
        {"name": "Maxwell", "position": "LB"},
        {"name": "Marco Verratti", "position": "CM"},
        {"name": "Blaise Matuidi", "position": "CM"},
        {"name": "Angel Di Maria", "position": "RW"},
        {"name": "Javier Pastore", "position": "CM"},
        {"name": "Zlatan Ibrahimovic", "position": "ST"},
        {"name": "Edinson Cavani", "position": "ST"},
    ],
    "psg_2025": [
        {"name": "Gianluigi Donnarumma", "position": "GK"},
        {"name": "Achraf Hakimi", "position": "RB"},
        {"name": "Marquinhos", "position": "CB"},
        {"name": "Nuno Mendes", "position": "LB"},
        {"name": "Vitinha", "position": "CM"},
        {"name": "Joao Neves", "position": "CM"},
        {"name": "Fabian Ruiz", "position": "CM"},
        {"name": "Ousmane Dembele", "position": "RW"},
        {"name": "Desire Doue", "position": "LW"},
        {"name": "Bradley Barcola", "position": "LW"},
        {"name": "Khvicha Kvaratskhelia", "position": "LW"},
    ],

    "galatasaray_legends": [
        {"name": "Claudio Taffarel", "position": "GK"},
        {"name": "Gheorghe Popescu", "position": "CB"},
        {"name": "Bülent Korkmaz", "position": "CB"},
        {"name": "Hakan Ünsal", "position": "LB"},
        {"name": "Sabri Sarıoğlu", "position": "RB"},
        {"name": "Felipe Melo", "position": "CM"},
        {"name": "Tugay Kerimoğlu", "position": "CM"},
        {"name": "Gheorghe Hagi", "position": "CM"},
        {"name": "Arda Turan", "position": "LW"},
        {"name": "Wesley Sneijder", "position": "RW"},
        {"name": "Mauro Icardi", "position": "ST"},
    ],
    "fenerbahce_legends": [
        {"name": "Volkan Demirel", "position": "GK"},
        {"name": "Lugano", "position": "CB"},
        {"name": "Can Bartu", "position": "CB"},
        {"name": "Roberto Carlos", "position": "LB"},
        {"name": "Gökhan Gönül", "position": "RB"},
        {"name": "Alex de Souza", "position": "CM"},
        {"name": "Emre Belözoğlu", "position": "CM"},
        {"name": "Oğuz Çetin", "position": "CM"},
        {"name": "Dirk Kuyt", "position": "LW"},
        {"name": "Jay-Jay Okocha", "position": "RW"},
        {"name": "Aykut Kocaman", "position": "ST"},
    ],
    "besiktas_legends": [
        {"name": "Rüştü Reçber", "position": "GK"},
        {"name": "Daniel Amokachi", "position": "CB"},
        {"name": "Samet Aybaba", "position": "CB"},
        {"name": "Tomas Sivok", "position": "LB"},
        {"name": "Serdar Kurtuluş", "position": "RB"},
        {"name": "Sergen Yalçın", "position": "CM"},
        {"name": "Atiba Hutchinson", "position": "CM"},
        {"name": "Josef de Souza", "position": "CM"},
        {"name": "Ricardo Quaresma", "position": "LW"},
        {"name": "Metin Tekin", "position": "RW"},
        {"name": "Mario Gomez", "position": "ST"},
    ],
    "belgium_golden_generation": [
        {"name": "Thibaut Courtois", "position": "GK"},
        {"name": "Toby Alderweireld", "position": "CB"},
        {"name": "Vincent Kompany", "position": "CB"},
        {"name": "Jan Vertonghen", "position": "LB"},
        {"name": "Thomas Meunier", "position": "RB"},
        {"name": "Axel Witsel", "position": "CM"},
        {"name": "Kevin De Bruyne", "position": "CM"},
        {"name": "Youri Tielemans", "position": "CM"},
        {"name": "Eden Hazard", "position": "LW"},
        {"name": "Dries Mertens", "position": "RW"},
        {"name": "Romelu Lukaku", "position": "ST"},
    ],
}

ROLE_ALIASES = {
    "GK": ["GK"],
    "CB": ["CB"],
    "FB": ["LB", "RB"],
    "CM": ["CM", "CDM", "CAM"],
    "LW": ["LW"],
    "RW": ["RW"],
    "ST": ["ST", "CF", "SS"],
}

BASE_SCORES = {
    "GK": 86,
    "RB": 73,
    "CB": 78,
    "LB": 73,
    "CDM": 76,
    "CM": 79,
    "CAM": 82,
    "RW": 77,
    "LW": 77,
    "ST": 81,
    "CF": 80,
    "SS": 80,
}

ATTRIBUTE_BASES = {
    "GK": {"attack": 18, "midfield": 38, "defense": 94},
    "RB": {"attack": 42, "midfield": 62, "defense": 82},
    "CB": {"attack": 24, "midfield": 48, "defense": 92},
    "LB": {"attack": 42, "midfield": 62, "defense": 82},
    "CDM": {"attack": 50, "midfield": 84, "defense": 78},
    "CM": {"attack": 66, "midfield": 88, "defense": 68},
    "CAM": {"attack": 84, "midfield": 90, "defense": 50},
    "RW": {"attack": 92, "midfield": 68, "defense": 35},
    "LW": {"attack": 92, "midfield": 68, "defense": 35},
    "ST": {"attack": 96, "midfield": 52, "defense": 32},
    "CF": {"attack": 92, "midfield": 62, "defense": 35},
    "SS": {"attack": 88, "midfield": 72, "defense": 38},
}

STAR_PLAYERS = [
    "Messi", "Ronaldo", "Henry", "Zidane", "Xavi", "Iniesta", "Modric", "Kroos",
    "Maldini", "Nesta", "Baresi", "Vieira", "Beckham", "Pirlo", "Neuer", "Lewandowski",
    "Haaland", "Van Dijk", "Rodri", "Bellingham", "Mbappe", "Osimhen", "Vini",
    "Hagi", "Sneijder", "Alex", "Hazard", "Lukaku", "Icardi", "Roberto Carlos",
    "Taffarel", "Kompany", "Courtois", "Tugay"
]


@dataclass
class PlayerProfile:
    attack: int
    midfield: int
    defense: int
    overall: int


def display_slot(slot_id: str) -> str:
    for slot in SLOT_DEFS:
        if slot["id"] == slot_id:
            return slot["label"]
    return slot_id


def slot_matches(position: str, slot_group: str) -> bool:
    return position in ROLE_ALIASES.get(slot_group, [slot_group])


def name_hash(text: str) -> int:
    h = 0
    for ch in text:
        h = (h * 31 + ord(ch)) % 100000
    return h


def player_profile(player: Dict[str, str], team_id: str) -> PlayerProfile:
    base = BASE_SCORES.get(player["position"], 72)
    anchors = ATTRIBUTE_BASES.get(player["position"], {"attack": 60, "midfield": 60, "defense": 60})
    h = name_hash(f"{team_id}:{player['name']}")
    variance = ((h % 13) - 6) * 2
    star_boost = 6 if any(token.lower() in player["name"].lower() for token in STAR_PLAYERS) else 0
    team_boost = ((h % 7) - 3) * 1.5

    attack = max(20, min(99, anchors["attack"] + variance + star_boost + team_boost))
    midfield = max(20, min(99, anchors["midfield"] + variance * 0.8 + star_boost * 0.6 + team_boost))
    defense = max(20, min(99, anchors["defense"] + variance * 0.6 + star_boost * 0.35 + team_boost))
    overall = max(20, min(99, base + variance + star_boost + team_boost))

    return PlayerProfile(attack=round(attack), midfield=round(midfield), defense=round(defense), overall=round(overall))


def get_open_slot_ids_for_player(position: str, filled_slots: List[str]) -> List[str]:
    open_ids = []
    for slot in SLOT_DEFS:
        if slot["id"] in filled_slots:
            continue
        if slot_matches(position, slot["group"]):
            open_ids.append(slot["id"])
    return open_ids


def get_assignable_slot_index(position: str, filled_slots: List[str]) -> int:
    open_ids = get_open_slot_ids_for_player(position, filled_slots)
    if not open_ids:
        return -1
    for idx, slot in enumerate(SLOT_DEFS):
        if slot["id"] == open_ids[0]:
            return idx
    return -1


def has_open_slot_for_player(position: str, filled_slots: List[str]) -> bool:
    return len(get_open_slot_ids_for_player(position, filled_slots)) > 0


def calculate_results(picks: List[Dict]) -> Dict:
    attack_pool = [p for p in picks if p["position"] in {"RW", "LW", "ST", "CF", "SS", "CAM"}]
    midfield_pool = [p for p in picks if p["position"] in {"CM", "CDM", "CAM"}]
    defense_pool = [p for p in picks if p["position"] in {"GK", "RB", "CB", "LB", "CDM"}]

    attack_ratings = [p["profile"].attack for p in attack_pool]
    midfield_ratings = [p["profile"].midfield for p in midfield_pool]
    defense_ratings = [p["profile"].defense for p in defense_pool]
    all_ratings = [p["profile"].overall for p in picks]

    attack = sum(attack_ratings) / len(attack_ratings) if attack_ratings else 0
    midfield = sum(midfield_ratings) / len(midfield_ratings) if midfield_ratings else 0
    defense = sum(defense_ratings) / len(defense_ratings) if defense_ratings else 0
    avg = sum(all_ratings) / len(all_ratings)
    spread = math.sqrt(sum((x - avg) ** 2 for x in all_ratings) / len(all_ratings))
    chemistry = max(45, min(99, 100 - spread))
    overall = attack * 0.38 + midfield * 0.27 + defense * 0.25 + chemistry * 0.10

    return {
        "attack": round(attack),
        "midfield": round(midfield),
        "defense": round(defense),
        "chemistry": round(chemistry),
        "overall": round(overall, 1),
        "avg_rating": avg,
    }


def score_tier(score: float) -> str:
    if score >= 95:
        return "GOAT TIER"
    if score >= 90:
        return "LEGENDARY"
    if score >= 85:
        return "ELITE"
    if score >= 80:
        return "WORLD CLASS"
    if score >= 75:
        return "VERY GOOD"
    return "MID TABLE FC"


def compute_achievements(stats: Dict, picks: List[Dict]) -> List[str]:
    achievements = []
    if stats["overall"] >= 95:
        achievements.append("Invincible Potential")
    if stats["attack"] >= 90:
        achievements.append("Firepower")
    if stats["midfield"] >= 90:
        achievements.append("Midfield Kings")
    if stats["defense"] >= 90:
        achievements.append("Iron Wall")
    if stats["chemistry"] >= 92:
        achievements.append("Well Drilled")
    if sum(1 for p in picks if p["profile"].overall >= 92) >= 3:
        achievements.append("Galacticos")
    return achievements


def build_insights(picks: List[Dict], stats: Dict) -> Dict:
    metric_rows = [
        {"key": "attack", "label": "Attack", "value": stats["attack"]},
        {"key": "midfield", "label": "Midfield", "value": stats["midfield"]},
        {"key": "defense", "label": "Defense", "value": stats["defense"]},
        {"key": "chemistry", "label": "Chemistry", "value": stats["chemistry"]},
    ]
    strongest = max(metric_rows, key=lambda x: x["value"])
    weakest = min(metric_rows, key=lambda x: x["value"])
    draft_mvp = max(picks, key=lambda p: p["profile"].overall)
    achievements = compute_achievements(stats, picks)
    return {"strongest": strongest, "weakest": weakest, "draft_mvp": draft_mvp, "achievements": achievements}


def start_state():
    if "picked" not in st.session_state:
        st.session_state.picked = []
    if "rolled_team_id" not in st.session_state:
        st.session_state.rolled_team_id = None
    if "status" not in st.session_state:
        st.session_state.status = "Click Roll Team to begin."
    if "results" not in st.session_state:
        st.session_state.results = None


def reset_game():
    st.session_state.picked = []
    st.session_state.rolled_team_id = None
    st.session_state.status = "Click Roll Team to begin."
    st.session_state.results = None


def roll_team():
    picked = st.session_state.picked
    filled_slots = [p["slot_id"] for p in picked]
    used_names = [p["name"] for p in picked]
    remaining = len(SLOT_DEFS) - len(picked)
    if remaining <= 0:
        return

    available_teams = []
    for team in TEAMS:
        roster = TEAM_PLAYERS.get(team["id"], [])
        if any((player["name"] not in used_names) and has_open_slot_for_player(player["position"], filled_slots) for player in roster):
            available_teams.append(team)

    if not available_teams:
        st.session_state.status = "No teams left with any usable players. Reset and try again."
        st.session_state.rolled_team_id = None
        return

    team = random.choice(available_teams)
    st.session_state.rolled_team_id = team["id"]
    st.session_state.status = f"Rolled {team['name']} ({team['era']}). Pick any player from that roster."


def pick_player(player: Dict[str, str]):
    team_id = st.session_state.rolled_team_id
    if not team_id:
        return
    picked = st.session_state.picked
    used_names = [p["name"] for p in picked]
    filled_slots = [p["slot_id"] for p in picked]

    if player["name"] in used_names:
        st.session_state.status = "That player has already been picked."
        return

    if not has_open_slot_for_player(player["position"], filled_slots):
        st.session_state.status = f"You already filled every {player['position']} / compatible slot."
        return

    slot_index = get_assignable_slot_index(player["position"], filled_slots)
    if slot_index == -1:
        st.session_state.status = f"No open slot fits {player['name']}."
        return

    profile = player_profile(player, team_id)
    next_picks = picked + [{
        **player,
        "team_id": team_id,
        "slot_id": SLOT_DEFS[slot_index]["id"],
        "profile": profile,
    }]
    st.session_state.picked = next_picks
    st.session_state.rolled_team_id = None
    st.session_state.status = "Click Roll Team for the next pick." if len(next_picks) < len(SLOT_DEFS) else "Team complete."

    if len(next_picks) == len(SLOT_DEFS):
        stats = calculate_results(next_picks)
        insights = build_insights(next_picks, stats)
        st.session_state.results = {"stats": stats, **insights}


start_state()

st.markdown(
    """
    <style>
        .block-container { padding-top: 1.5rem; }
        .stButton > button { border-radius: 14px; padding: 0.75rem 1.1rem; font-weight: 700; }
        .metric-card { background: #0f172a; padding: 1rem; border-radius: 16px; border: 1px solid #1f2937; }
        .pill { display: inline-block; padding: 0.35rem 0.75rem; border-radius: 999px; border: 1px solid #334155; margin: 0.2rem 0.25rem 0 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Football Draft MVP")
st.caption("Roll a team, then pick any player from that roster. A player can only be selected if an open compatible slot still exists.")

col_left, col_right = st.columns([0.30, 0.70], gap="large")

with col_left:
    st.markdown("### Controls")
    st.write(st.session_state.status)

    if st.button("Roll Team", use_container_width=True, disabled=len(st.session_state.picked) >= len(SLOT_DEFS)):
        roll_team()
        st.rerun()

    if st.button("Reset", use_container_width=True):
        reset_game()
        st.rerun()

    st.markdown("### Progress")
    picked_count = len(st.session_state.picked)
    st.write(f"**{picked_count} / {len(SLOT_DEFS)} picks**")
    st.progress(picked_count / len(SLOT_DEFS))
    st.write(f"**Open slots:** {len(SLOT_DEFS) - picked_count}")

    st.markdown("### Locked lineup")
    picks_by_slot = {p["slot_id"]: p for p in st.session_state.picked}
    for slot in SLOT_DEFS:
        player_name = picks_by_slot.get(slot["id"], {}).get("name", "—")
        st.markdown(f"**{slot['label']}**: {player_name}")

with col_right:
    current_team = next((t for t in TEAMS if t["id"] == st.session_state.rolled_team_id), None)

    if not st.session_state.results:
        st.markdown("### Current round")
        if current_team:
            st.subheader(f"Rolled: {current_team['name']}")
            st.write(f"{current_team['era']} • {current_team['league']}")
            st.write("Full roster is shown below. Green buttons are currently usable.")

            roster = TEAM_PLAYERS.get(current_team["id"], [])
            filled_slots = [p["slot_id"] for p in st.session_state.picked]
            used_names = [p["name"] for p in st.session_state.picked]

            cols = st.columns(3)
            for i, player in enumerate(roster):
                is_used = player["name"] in used_names
                eligible = (not is_used) and has_open_slot_for_player(player["position"], filled_slots)
                slot_index = get_assignable_slot_index(player["position"], filled_slots)
                slot_label = "No open slot" if slot_index == -1 else SLOT_DEFS[slot_index]["label"]

                with cols[i % 3]:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    st.markdown(f"**{player['name']}**")
                    st.caption(f"{player['position']} • {('Already picked' if is_used else slot_label)}")
                    if st.button("Pick", key=f"pick_{current_team['id']}_{player['name']}", disabled=not eligible, use_container_width=True):
                        pick_player(player)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Click **Roll Team** to reveal the club for this pick.")
    else:
        stats = st.session_state.results["stats"]
        insights = st.session_state.results

        st.markdown("### Final result")
        st.markdown(
            f"""
            <div class='metric-card'>
                <h1 style='margin:0;'>Draft complete</h1>
                <h2 style='color:#10b981; margin:0.5rem 0 0;'>Greatness score: {stats['overall']}</h2>
                <p style='margin:0.25rem 0 0; font-weight:700;'>{score_tier(stats['overall'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        a1, a2, a3, a4 = st.columns(4)
        with a1:
            st.metric("Attack", stats["attack"])
        with a2:
            st.metric("Midfield", stats["midfield"])
        with a3:
            st.metric("Defense", stats["defense"])
        with a4:
            st.metric("Chemistry", stats["chemistry"])

        b1, b2 = st.columns(2)
        with b1:
            st.markdown("### Biggest strength")
            st.write(f"**{insights['strongest']['label']}** — {insights['strongest']['value']}/100")
            st.markdown("### Draft MVP")
            mvp = insights["draft_mvp"]
            st.write(f"**{mvp['name']}**")
            st.caption(f"{mvp['position']} • Rating {mvp['profile'].overall}")
        with b2:
            st.markdown("### Biggest weakness")
            st.write(f"**{insights['weakest']['label']}** — {insights['weakest']['value']}/100")

        st.markdown("### Achievements")
        if insights["achievements"]:
            for achievement in insights["achievements"]:
                st.markdown(f"<span class='pill'>{achievement}</span>", unsafe_allow_html=True)
        else:
            st.write("No achievements this run.")

        st.markdown("### Your XI")
        picks_by_slot = {p["slot_id"]: p for p in st.session_state.picked}
        for slot in SLOT_DEFS:
            st.write(f"**{slot['label']}**: {picks_by_slot.get(slot['id'], {}).get('name', '—')}")

        st.markdown("### Stat breakdown")
        st.write(f"Attack: {stats['attack']}")
        st.write(f"Midfield: {stats['midfield']}")
        st.write(f"Defense: {stats['defense']}")
        st.write(f"Chemistry: {stats['chemistry']}")

        if st.button("Play again"):
            reset_game()
            st.rerun()

st.markdown("---")
st.caption("This is a single-file Streamlit version you can open in PyCharm and run locally.")
