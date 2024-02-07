import psycopg2
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from openpyxl import load_workbook
from openpyxl.styles.fills import PatternFill
from openpyxl.styles import Font
from datetime import datetime
import math


data_do_dia = datetime.today().strftime('%d-%m-%Y')

local_db = psycopg2.connect(
    user="postgres",
    password="Santos010802.",
    host="localhost",
    port="5432",
    database="postgres")



class Database:

    def __init__(self):
        self.engine_local = None
        self.chromedriver = webdriver.Chrome(executable_path=r"C:\\Users\\Joao Luiz\\Downloads\\ChromeDriver.exe")

    def conexao_db(self)-> None:
        for rec in range(3):
            try:
                self.engine_local = create_engine('postgresql://postgres:Santos010802.@localhost:5432')
            except Exception as e:
                print(f"\nError:>>> Tentativa {rec} de reconexão")
                sleep(3)
                continue
            return self.engine_local
        

class CapturaStats:

    def __init__(self):
        self.connection = Database()

    def verificar_tabela_se_existe(self, nome_tabela):
        try:
            query = pd.read_sql_table(f'tbl_all_seasons_teams_stats', self.connection.conexao_db())
            return True
        except:
            return False
    

    def captura_stats_teams_all_seasons(self):

        checa_se_tbl_existe = self.verificar_tabela_se_existe('tbl_all_seasons_teams_stats')
        if checa_se_tbl_existe:
            cursor = local_db.cursor()
            sleep(1.5)
            cursor.execute('DROP TABLE tbl_all_seasons_teams_stats')
            local_db.commit()
            print('\nDatabase antigo excluido!')
        else:
            pass

        
        #print('\nNavegador Iniciado')

        # Seasons
        seasons_passadas = ['S14', 'S13', 'S12', 'S11']
        for season in seasons_passadas:
            
            # link para pegar todos os splits e camps
            self.connection.chromedriver.get(f"https://gol.gg/teams/list/season-{season}/split-ALL/tournament-ALL/")
            sleep(3)

            # ler tabela
            tabela = self.connection.chromedriver.find_element(By.XPATH, "/html/body/div/main/div[2]/div/div[2]/div/table")
            html_content = tabela.get_attribute("outerHTML")
            bs = BeautifulSoup(html_content, 'html.parser')
            table = bs.find(name="table")
            tabela_lida = pd.read_html(str(table), flavor='html5lib')[0]

           
            # CBLOL
            tabela_lida.loc[tabela_lida['Name'] == 'Vivo Keyd', 'Name'] = 'Vivo Keyd Stars'
            tabela_lida.loc[tabela_lida['Name'] == 'Vorax Liberty', 'Name'] = 'Liberty'
            tabela_lida.loc[tabela_lida['Name'] == 'Vorax Academy', 'Name'] = 'Liberty Academy'
            tabela_lida.loc[tabela_lida['Name'] == 'FURIA Uppercut', 'Name'] = 'FURIA Esports'
            tabela_lida.loc[tabela_lida['Name'] == 'Havan Liberty Gaming', 'Name'] = 'Liberty Academy'
            tabela_lida.loc[tabela_lida['Name'] == 'INTZ eSports', 'Name'] = 'INTZ e-Sports'


            # LPL
            tabela_lida.loc[tabela_lida['Name'] == 'Suning Gaming', 'Name'] = 'Weibo Gaming'
            tabela_lida.loc[tabela_lida['Name'] == 'Suning', 'Name'] = 'Weibo Gaming'
            tabela_lida.loc[tabela_lida['Name'] == 'Bilibili Live', 'Name'] = 'Bilibili Gaming'
            tabela_lida.loc[tabela_lida['Name'] == 'Victory Five', 'Name'] = 'Ninjas in Pyjamas'
            tabela_lida.loc[tabela_lida['Name'] == 'Rogue Warriors', 'Name'] = 'Anyone s Legend'


            # LCK -> Feito
            tabela_lida.loc[tabela_lida['Name'] == 'DAMWON Gaming', 'Name'] = 'Dplus KIA'
            tabela_lida.loc[tabela_lida['Name'] == 'DWG KIA', 'Name'] = 'Dplus KIA'
            tabela_lida.loc[tabela_lida['Name'] == 'SK Telecom T1', 'Name'] = 'T1'
            tabela_lida.loc[tabela_lida['Name'] == 'Fredit BRION', 'Name'] = 'OK BRION'
            tabela_lida.loc[tabela_lida['Name'] == 'hyFresh Blade', 'Name'] = 'OK BRION'
            tabela_lida.loc[tabela_lida['Name'] == 'Kongdoo Monster', 'Name'] = 'OK BRION'
            tabela_lida.loc[tabela_lida['Name'] == 'BRION', 'Name'] = 'OK BRION'
            tabela_lida.loc[tabela_lida['Name'] == 'Samsung Galaxy', 'Name'] = 'Gen.G eSports'
            tabela_lida.loc[tabela_lida['Name'] == 'KSV eSports', 'Name'] = 'Gen.G eSports'
            tabela_lida.loc[tabela_lida['Name'] == 'Afreeca Freecs', 'Name'] = 'Kwangdong Freecs'  
            tabela_lida.loc[tabela_lida['Name'] == 'Afreeca Challengers', 'Name'] = 'KDF Challengers'
            tabela_lida.loc[tabela_lida['Name'] == 'Liiv SANDBOX', 'Name'] = 'FearX'
            tabela_lida.loc[tabela_lida['Name'] == 'Sandbox Gaming', 'Name'] = 'FearX'
            tabela_lida.loc[tabela_lida['Name'] == 'LSB Challengers', 'Name'] = 'FearX Challengers'
            tabela_lida.loc[tabela_lida['Name'] == 'Kingzone DragonX', 'Name'] = 'DRX'
            tabela_lida.loc[tabela_lida['Name'] == 'DragonX', 'Name'] = 'DRX'


            # EUW
            tabela_lida.loc[tabela_lida['Name'] == 'Astralis Talent', 'Name'] = 'Astralis'
            tabela_lida.loc[tabela_lida['Name'] == 'Fnatic Rising', 'Name'] = 'Fnatic'
            tabela_lida.loc[tabela_lida['Name'] == 'exceL eSports', 'Name'] = 'GIANTX'
            tabela_lida.loc[tabela_lida['Name'] == 'Excel Esports', 'Name'] = 'GIANTX'
            tabela_lida.loc[tabela_lida['Name'] == 'MAD Lions', 'Name'] = 'MAD Lions KOI'
            tabela_lida.loc[tabela_lida['Name'] == 'MAD Lions E.C.', 'Name'] = 'MAD Lions KOI'
            tabela_lida.loc[tabela_lida['Name'] == 'BT Excel', 'Name'] = 'JD|XL'


            # NA
            tabela_lida.loc[tabela_lida['Name'] == 'FlyQuest Academy', 'Name'] = 'FlyQuest Challengers'
            tabela_lida.loc[tabela_lida['Name'] == 'Immortals Academy', 'Name'] = 'Immortals Challengers'
            tabela_lida.loc[tabela_lida['Name'] == 'Team Liquid Academy', 'Name'] = 'Team Liquid Challengers'
            tabela_lida.loc[tabela_lida['Name'] == 'TSM Academy', 'Name'] = 'TSM Challengers'
            tabela_lida.loc[tabela_lida['Name'] == 'Golden Guardians Academy', 'Name'] = 'Golden Guardians Challengers'
            tabela_lida.loc[tabela_lida['Name'] == 'Dignitas Academy', 'Name'] = 'Dignitas Challengers'
            tabela_lida.loc[tabela_lida['Name'] == 'Cloud9 Academy', 'Name'] = 'Cloud9 Challengers'
            tabela_lida.loc[tabela_lida['Name'] == 'CLG Academy', 'Name'] = 'CLG Challengers'
            tabela_lida.loc[tabela_lida['Name'] == '100 Thieves Academy', 'Name'] = '100 Challengers'
            tabela_lida.loc[tabela_lida['Name'] == 'Area of Effect Ginger Turmeric', 'Name'] = 'Area of Effect Esports'
            tabela_lida.loc[tabela_lida['Name'] == 'Evil Geniuses Academy', 'Name'] = 'Evil Geniuses Challengers'


            # ESLOL - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'Team 7AM', 'Name'] = 'One Way Esports'
            tabela_lida.loc[tabela_lida['Name'] == 'mCon LG UltraGear', 'Name'] = 'mCon esports'
            tabela_lida.loc[tabela_lida['Name'] == 'Sector One', 'Name'] = 'Benelux United' 


            # HITPOINT - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'ECLOT', 'Name'] = 'Dynamo Eclot'
            tabela_lida.loc[tabela_lida['Name'] == 'ECLOT Academy', 'Name'] = 'Dynamo Eclot Academy'
            tabela_lida.loc[tabela_lida['Name'] == 'Dynamo Esports', 'Name'] = 'Dynamo Eclot'

            # PRM - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'Mousesports', 'Name'] = 'MOUZ NXT'
            tabela_lida.loc[tabela_lida['Name'] == 'MOUZ', 'Name'] = 'MOUZ NXT'

            # SL - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'Movistar Riders', 'Name'] = 'Movistar KOI'
            tabela_lida.loc[tabela_lida['Name'] == 'UCAM Esports Club', 'Name'] = 'UCAM Tokiers'
            tabela_lida.loc[tabela_lida['Name'] == 'Giants', 'Name'] = 'GIANTX Pride'
            tabela_lida.loc[(tabela_lida['Name'] == 'Team Heretics') & (tabela_lida['Region'] == 'ES'), 'Name'] = 'Heretics Academy'

            # LFL - Feito
            tabela_lida.loc[(tabela_lida['Name'] == 'Karmine Corp') & (tabela_lida['Region'] == 'FR'), 'Name'] = 'Karmine Corp Blue'
            tabela_lida.loc[(tabela_lida['Name'] == 'Team BDS') & (tabela_lida['Region'] == 'FR'), 'Name'] = 'Team BDS Academy'
            tabela_lida.loc[tabela_lida['Name'] == 'Gamers Origin', 'Name'] = 'Team GO'
            tabela_lida.loc[tabela_lida['Name'] == 'Elyandra Esport', 'Name'] = 'Mirage Elyandra'

            # LIT - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'Cyberground Gaming', 'Name'] = 'EKO Academy'
            tabela_lida.loc[tabela_lida['Name'] == 'Outplayed', 'Name'] = 'aNc Outplayed'

            # LJL - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'Burning Core', 'Name'] = 'Burning Core Toyama'
            tabela_lida.loc[tabela_lida['Name'] == 'Rascal Jester', 'Name'] = 'FENNEL'

            # LAT - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'Rainbow7', 'Name'] = 'Movistar R7'

            # OCE - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'Legacy Esports', 'Name'] = 'Kanga Esports'

            # PCS - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'SEM9', 'Name'] = 'West Point Esports'
            tabela_lida.loc[tabela_lida['Name'] == 'SEM9 WPE', 'Name'] = 'West Point Esports'

            # UL - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'AGO ROGUE', 'Name'] = 'Alior Bank Team'
            tabela_lida.loc[tabela_lida['Name'] == 'Grypciocraft Esports', 'Name'] = 'GRP Esports'
            tabela_lida.loc[tabela_lida['Name'] == 'Maturalni Forsaken', 'Name'] = 'Forsaken'

            # LPLOL - Feito
            tabela_lida.loc[tabela_lida['Name'] == 'Byteway Esports', 'Name'] = 'BWE Esports'
            tabela_lida.loc[tabela_lida['Name'] == 'GTZ Bulls', 'Name'] = 'GTZ Esports'
            tabela_lida.loc[tabela_lida['Name'] == 'OFFSET Esports', 'Name'] = 'Keypulse Esports'

            # TCL - Feito
            tabela_lida.loc[tabela_lida['Name'] == '1907 Fenerbahce', 'Name'] = 'Fenerbahce Esports'
            tabela_lida.loc[tabela_lida['Name'] == 'SuperMassive Blaze', 'Name'] = 'Papara SuperMassive'

            # VCS
            tabela_lida.loc[tabela_lida['Name'] == 'MGN Box Esports', 'Name'] = 'MGN Blue Esports'
            tabela_lida.loc[tabela_lida['Name'] == 'Saigon Buffalo', 'Name'] = 'Vikings Esports'

            # Excluindo linhas - regioes que não existem mais
            tabela_lida.drop(tabela_lida[tabela_lida['Region'] == 'CIS'].index, inplace=True)
            tabela_lida.drop(tabela_lida[tabela_lida['Region'] == 'LT'].index, inplace=True)
            tabela_lida.drop(tabela_lida[tabela_lida['Region'] == 'NL'].index, inplace=True)

            # Alterando os nomes das region
            tabela_lida['Region'] = tabela_lida['Region'].fillna('NA')
            tabela_lida.loc[tabela_lida['Region'] == 'BE', 'Region'] = 'ESLOL'
            tabela_lida.loc[tabela_lida['Region'] == 'CZ', 'Region'] = 'HITPOINT'
            tabela_lida.loc[tabela_lida['Region'] == 'DE', 'Region'] = 'PRM'
            tabela_lida.loc[tabela_lida['Region'] == 'ES', 'Region'] = 'SUPERLIGA'
            tabela_lida.loc[tabela_lida['Region'] == 'FR', 'Region'] = 'LFL'
            tabela_lida.loc[tabela_lida['Region'] == 'GR', 'Region'] = 'GLL'
            tabela_lida.loc[tabela_lida['Region'] == 'IT', 'Region'] = 'LIT'
            tabela_lida.loc[tabela_lida['Region'] == 'JP', 'Region'] = 'LJL'
            tabela_lida.loc[tabela_lida['Region'] == 'PL', 'Region'] = 'UL'
            tabela_lida.loc[tabela_lida['Region'] == 'PT', 'Region'] = 'LPLOL'
            tabela_lida.loc[tabela_lida['Region'] == 'RS', 'Region'] = 'BALKAN'
            tabela_lida.loc[tabela_lida['Region'] == 'TR', 'Region'] = 'TCL'
            tabela_lida.loc[tabela_lida['Region'] == 'VN', 'Region'] = 'VCS'

            # Excluindo linhas de times que não existem mais
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Weibo Youth'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'West Point PH'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Shadow EK'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Shadow Battlica'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Hungkuang Falcon'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'DKJH'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Winthrop University'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Zoos Gaming'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Team Pending'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'No Team'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Resolve NA'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'No Org'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Barrage.NA'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'DK Crew'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'K1CK'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'No Name Esport'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Plonace Garnitury'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'piratesports'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Barrage Esports'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Galaxy Racer EU'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Godsent'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Granit Gaming'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Nordavind'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Resolve'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Granit Gaming'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'HMG'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Huya All Star'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Legend Esport Gaming'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'LYA'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Shu Dai Xiong Gaming'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Team Pinnacle'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'Wahaha Gaming'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'WanZhen Esports Club'].index)
            tabela_lida = tabela_lida.drop(tabela_lida[tabela_lida['Name'] == 'WanZhen Esports Club'].index)

            #print(f'\n{tabela_lida}')

            tabela_lida.to_sql(f'tbl_all_seasons_teams_stats', self.connection.conexao_db(), if_exists='append')
            print(f'\nSeason {season} capturada!')



    def captura_stats_champions_all_seasons(self):

        checa_se_tbl_existe = self.verificar_tabela_se_existe('tbl_all_seasons_champions_stats')
        if checa_se_tbl_existe:
            cursor = local_db.cursor()
            sleep(1.5)
            cursor.execute('DROP TABLE tbl_all_seasons_champions_stats')
            local_db.commit()
            print('\nDatabase antigo excluido!')
        else:
            pass

        # link para pegar todos os splits e camps
        seasons_passadas = ['S14', 'S13', 'S12', 'S11', 'S10', 'S9', 'S8', 'S7']
        for season in seasons_passadas:
            self.connection.chromedriver.get(f"https://gol.gg/champion/list/season-{season}/split-ALL/tournament-ALL/")
            sleep(3)

            # ler tabela
            tabela = self.connection.chromedriver.find_element(By.XPATH, "/html/body/div/main/div[2]/div/div[2]/div/table")
            html_content = tabela.get_attribute("outerHTML")
            bs = BeautifulSoup(html_content, 'html.parser')
            table = bs.find(name="table")
            tabela_lida = pd.read_html(str(table), flavor='html5lib')[0]
            tabela_lida['Season'] = season

            tabela_lida.to_sql(f'tbl_all_seasons_champions_stats', self.connection.conexao_db(), if_exists='append')
            print(f'\nSeason {season} capturada!')






def main():

    executar_captura = CapturaStats()

    executar_captura.captura_stats_teams_all_seasons()
    sleep(0.5)
    print('\n\nIniciando a captura dos champions')
    executar_captura.captura_stats_champions_all_seasons()



main()