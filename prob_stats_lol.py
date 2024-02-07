import PySimpleGUI as sg
from sqlalchemy import create_engine
from time import sleep  
import pandas as pd
import psycopg2
from scipy.stats import poisson
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler, Imputer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

local_db = psycopg2.connect(
    user="postgres",
    password="Santos010802.",
    host="localhost",
    port="5432",
    database="postgres")




class Database:

    def __init__(self):
        self.engine_local = None


    def conexao_db(self)-> None:
        for rec in range(3):
            try:
                self.engine_local = create_engine('postgresql://postgres:Santos010802.@localhost:5432')
            except Exception as e:
                print(f"\nError:>>> Tentativa {rec} de reconexão")
                sleep(3)
                continue
            return self.engine_local
        

    def base_iteracao(self):
        while True:
            try:
                base = pd.read_sql_query(""" SELECT * FROM "public".tbl_all_seasons_teams_stats """, self.conexao_db())
                base_db = pd.DataFrame(base)
                break
            except:
                sleep(0.5)
        return base_db


    def stats_team_geral(self, team, region):
        while True:
            try:
                base = pd.read_sql_query(f""" SELECT "Name", "Region",
                                                SUM("Games") as sum_jogos,
                                                ROUND(CAST(AVG(CAST(REPLACE("Win rate", '%', '') AS numeric)) AS numeric), 2) as avg_win_rate,
                                                ROUND(AVG("GPM"), 2) as avg_gpm,
                                                ROUND(AVG(CAST("GDM" AS numeric)), 2) AS avg_gold_dif_minute,
                                                ROUND(CAST(AVG(CAST(REPLACE("Game duration", ':', '.') AS numeric)) AS numeric), 2) as avg_game_time,
                                                ROUND(AVG(CAST("Kills / game" AS numeric)), 2) AS avg_kills_per_game,
                                                ROUND(AVG(CAST("Deaths / game" AS numeric)), 2) AS avg_deaths_per_game,
                                                ROUND(AVG(CAST("Towers killed" AS numeric)), 2) AS avg_towers_feita_per_game,
                                                ROUND(AVG(CAST("Towers lost" AS numeric)), 2) AS avg_towers_sofridas_per_game,
                                                ROUND(AVG(CAST("FB%" AS numeric)), 2) AS avg_first_blood,
                                                ROUND(AVG(CAST("FT%" AS numeric)), 2) AS avg_first_tower,
                                                ROUND(AVG(CAST("DRAPG" AS numeric)), 2) AS avg_drags_killer_per_game,
                                                ROUND(AVG(CAST("DRA@15" AS numeric)), 2) AS avg_drags_at_15min,
                                                SUM(CAST("GD@15" AS numeric)) AS sum_gold_dif_15, ROUND(AVG(CAST("GD@15" AS numeric)), 2) AS avg_gold_dif_15,
                                                ROUND(AVG(CAST("NASHPG" AS numeric)), 2) AS avg_nash_per_game,
                                                ROUND(AVG("DPM"), 2) as avg_damage_to_champs_per_minute
                                                FROM "public".tbl_all_seasons_teams_stats
                                                WHERE "Name" = '{team}'
                                                AND "Region" = '{region}'
                                                GROUP BY "Name", "Region";  """, self.conexao_db())
                base_team = pd.DataFrame(base)
                break
            except:
                sleep(0.5)
        return base_team
    

    def stats_team_season_atual(self, team, region, season_atual='S14'):
        while True:
            try:
                base = pd.read_sql_query(f""" SELECT *
                                              FROM "public".tbl_all_seasons_teams_stats
                                              WHERE "Name" = '{team}'
                                              AND "Region" = '{region}'
                                              AND "Season" = '{season_atual}';  """, self.conexao_db())
                base_team_season_atual = pd.DataFrame(base)
                break
            except:
                sleep(0.5)
        return base_team_season_atual
    

    def return_ligas(self):
        while True:
            try:
                base = pd.read_sql_query(f""" SELECT DISTINCT("Region") FROM "public".tbl_all_seasons_teams_stats ORDER BY "Region"  """, self.conexao_db())
                base_ligas = pd.DataFrame(base)
                break
            except:
                sleep(0.5)
        return base_ligas











class Projeto:

    def __init__(self):
        self.connection = Database()
        self.ligas = []
        self.base_iteracao = []
        self.lista_ligas = {}
        self.team_a_geral = None
        self.team_b_geral = None
        self.team_a_atual = None
        self.team_b_atual = None
    

    def captura_prob_times_escolhidos(self, liga_selecionada, home, away):
        

        ### CAPTURA AS INFORMAÇÕES DOS DOIS TIMES - TANTO GERAL, QUANTO DA SEASON ATUAL APENAS ###
        ## Stats team a - Home
        self.team_a_geral = self.connection.stats_team_geral(team=home, region=liga_selecionada)
        self.team_a_atual = self.connection.stats_team_season_atual(team=home, region=liga_selecionada)

        ## Stats team b - Away
        self.team_b_geral = self.connection.stats_team_geral(team=away, region=liga_selecionada)
        self.team_b_atual = self.connection.stats_team_season_atual(team=home, region=liga_selecionada)



























    def validar_selecao(self, liga, time_a, time_b, kills_escolhida):
        if liga and time_a and time_b:
            sg.popup_timed("Iniciando o prognóstico da partida. Aguarde um pouco!", title='Prognostico do Confronto',
                        auto_close_duration=1)
            variavel = self.captura_prob_times_escolhidos(liga_selecionada=liga, home=time_a, away=time_b, kill_escolhida=kills_escolhida)
            if variavel:
                pass
            else:
                sg.popup_timed("Erro nos calculos! Tente novamente daqui a pouco o confronto", title='Erro nos calculos',
                            auto_close_duration=1.5)
        elif time_a == time_b and time_a != "":
            sg.popup_timed("O time mandante e o time visitante devem ser diferentes.", title='Erro de Seleção',
                        auto_close_duration=5)
        else:
            sg.popup_timed("Por favor, selecione todas as opções.", title='Erro de Seleção', auto_close_duration=5)



    def layout_principal(self):
        
        self.ligas = self.connection.return_ligas()['Region']

        self.ligas = self.ligas.sort_values().reset_index(drop=True)

        self.base_iteracao = self.connection.base_iteracao()


        for camp in self.ligas:
            list_teams = list(set(self.base_iteracao.loc[self.base_iteracao['Region'] == f'{camp}', 'Name'].unique()))
            self.lista_ligas[camp] = list_teams


        sg.theme('GreenTan')
        layout_left = [
            [sg.Image(filename='C:/Users/Joao Luiz/Documents/icons/teste.png', size=(400, 266))]
        ]
        layout_right = [
            [sg.Text('Escolha uma liga:', font=('Calibri', 12, 'italic', 'bold'))], [sg.Combo(list(self.lista_ligas.keys()), key='-LIGA-', font=('Calibri', 11), enable_events=True, size=(25, 1))],
            [sg.Text('Escolha o time A:', font=('Calibri', 12, 'italic', 'bold'))], [sg.Combo([], key='-TIME_A-', font=('Calibri', 11), enable_events=True, size=(25, 1))],
            [sg.Text('Escolha o time B:', font=('Calibri', 12, 'italic', 'bold'))], [sg.Combo([], key='-TIME_B-', font=('Calibri', 11), enable_events=True, size=(25, 1))],
            [sg.Push(), sg.Button('Confirmar', font=('Calibri', 10, 'bold'), key='-CONFIRMAR-', pad=((0, 10), 5)), sg.Push(),
            sg.Button('Atualizar', font=('Calibri', 10, 'bold'), key='-ATUALIZAR-'), sg.Push()],
            [sg.Push(), sg.Button('Exportar', font=('Calibri', 10, 'bold'), key='-EXPORTAR-', pad=((0, 10), 5)), sg.Push()]
        ]

        layout = [
            [sg.Column(layout_left), sg.VSeparator(), sg.Column(layout_right)]
        ]
        
        return layout
    

    def mostrar_layout_principal(self, layout):

        window = sg.Window('LoL - Prognóstico do Confronto', layout,
                   icon='C:/Users/Joao Luiz/Documents/icons/video-game-controller.ico')
        
        while True:
            event, values = window.read()
            
            if event == sg.WINDOW_CLOSED:
                break

            elif event == '-CONFIRMAR-':
                liga = values['-LIGA-'] 
                time_a = values['-TIME_A-']
                time_b = values['-TIME_B-']
                self.validar_selecao(liga, time_a, time_b)

            elif event == '-EXPORTAR-':
                # Extrair a tabela de confrontos escolhidos no BD depois de fechar a interface gráfica
                pass

            elif event == '-LIGA-':
                times = self.lista_ligas[values['-LIGA-']]
                times_sorted = sorted(times)  # Sort the list alphabetically
                window['-TIME_A-'].update(values=times_sorted)
                window['-TIME_B-'].update(values=times_sorted)

            elif event == '-TIME_A-' or event == '-TIME_B-':
                time_a = values['-TIME_A-']
                time_b = values['-TIME_B-']
                if time_a == time_b:
                    pass
                    #self.validar_selecao(None, time_a, time_b)

            elif event == '-ATUALIZAR-':
                # Atualizar o layout
                window['-LIGA-'].update("")
                window['-TIME_A-'].update("")
                window['-TIME_B-'].update("")
                # ...
                pass

        window.close()








def main():

    executar_layout = Projeto()

    executar_layout.mostrar_layout_principal(executar_layout.layout_principal())





main()