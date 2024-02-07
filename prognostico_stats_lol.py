import PySimpleGUI as sg
from sqlalchemy import create_engine
from time import sleep  
import pandas as pd
import psycopg2
from scipy.stats import poisson
import matplotlib.pyplot as plt
import numpy as np


LISTA_KILLS = ['18,5', '19,5', '20,5', '21,5', '22,5', '23,5', '24,5', '25,5', '26,5', '27,5', '28,5', '29,5', '30,5', '31,5', '32,5']

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
                base = pd.read_sql_query(""" SELECT * FROM "public".tbl_stats_teams_lol """, self.conexao_db())
                base_db = pd.DataFrame(base)
                break
            except:
                sleep(0.5)
        return base_db
    

    def stats_team(self, team):
        while True:
            try:
                base = pd.read_sql_query(f""" SELECT * FROM "public".tbl_stats_teams_lol WHERE "Time" = '{team}'; """, self.conexao_db())
                base_team = pd.DataFrame(base)
                break
            except:
                sleep(0.5)
        return base_team
    
    def return_ligas(self):
        while True:
            try:
                base = pd.read_sql_query(f""" SELECT DISTINCT("Liga") FROM "public".tbl_stats_teams_lol  """, self.conexao_db())
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
        self.team_a = None
        self.team_b = None
    



    def captura_prob_times_escolhidos(self, liga_selecionada, home, away, kill_escolhida):
        

        ## Stats team a - Home
        self.team_a = self.connection.stats_team(team=home)
        #self.team_a = self.team_a.to_string(index=False)

        media_tempo_team_a = str(self.team_a['Avg Duração'].iloc[0])

            # Kills
        media_kills_indiv_team_a = str(self.team_a['Avg Kills Indiv'].iloc[0])
        media_kills_sofridas_team_a = str(self.team_a['Avg Kills Sofridas'].iloc[0])
        media_kills_team_a = str(self.team_a['Avg Kills'].iloc[0])

            # Torres
        media_torres_indiv_team_a = str(self.team_a['Avg Towers Indiv'].iloc[0])
        media_torres_sofridas_team_a = str(self.team_a['Avg Towers Sofridas'].iloc[0])
        media_torres_team_a = str(self.team_a['Avg towers'].iloc[0])

            # Drakes
        media_drakes_indiv_team_a = str(self.team_a['Avg drakes Indiv'].iloc[0])
        media_drakes_sofridos_team_a = str(self.team_a['Avg drakes sofridos'].iloc[0])
        media_drakes_team_a = str(self.team_a['Avg drakes'].iloc[0])

            # Porcentagens
        percentages_over_11_5_torres_team_a = str(self.team_a['% Over 11,5 torres'].iloc[0])
        percentages_over_12_5_torres_team_a = str(self.team_a['% Over 12,5 torres'].iloc[0])

        percentages_over_4_5_drakes_team_a = str(self.team_a['% Over 4,5 drakes'].iloc[0])
        percentages_over_5_5_drakes_team_a = str(self.team_a['% Over 5,5 drakes'].iloc[0])

        percentages_over_kill_escolhido_team_a = str(self.team_a[f'% Over {kill_escolhida}'].iloc[0])

        percentages_over_27_30_mins_team_a = str(self.team_a['% Under 27:30'].iloc[0])
        percentages_over_27_30_mins_team_a = (str(100 - float(percentages_over_27_30_mins_team_a.rstrip('%')))+'%').replace('.0', '')

        percentages_over_28_30_mins_team_a = str(self.team_a['% Under 28:30'].iloc[0])
        percentages_over_28_30_mins_team_a = (str(100 - float(percentages_over_28_30_mins_team_a.rstrip('%')))+'%').replace('.0', '')

        percentages_over_29_30_mins_team_a = str(self.team_a['% Under 29:30'].iloc[0])
        percentages_over_29_30_mins_team_a = (str(100 - float(percentages_over_29_30_mins_team_a.rstrip('%')))+'%').replace('.0', '')

        percentages_over_30_30_mins_team_a = str(self.team_a['% Under 30:30'].iloc[0])
        percentages_over_30_30_mins_team_a = (str(100 - float(percentages_over_30_30_mins_team_a.rstrip('%')))+'%').replace('.0', '')

        percentages_over_31_30_mins_team_a = str(self.team_a['% Under 31:30'].iloc[0])
        percentages_over_31_30_mins_team_a = (str(100 - float(percentages_over_31_30_mins_team_a.rstrip('%')))+'%').replace('.0', '')

        percentages_over_32_30_mins_team_a = str(self.team_a['% Under 32:30'].iloc[0])
        percentages_over_32_30_mins_team_a = (str(100 - float(percentages_over_32_30_mins_team_a.rstrip('%')))+'%').replace('.0', '')

        percentages_over_33_30_mins_team_a = str(self.team_a['% Under 33:30'].iloc[0])
        percentages_over_33_30_mins_team_a = (str(100 - float(percentages_over_33_30_mins_team_a.rstrip('%')))+'%').replace('.0', '')

        percentages_over_34_30_mins_team_a = str(self.team_a['% Under 34:30'].iloc[0])
        percentages_over_34_30_mins_team_a = (str(100 - float(percentages_over_34_30_mins_team_a.rstrip('%')))+'%').replace('.0', '')




        ## Stats team b - Away
        self.team_b = self.connection.stats_team(team=away)

        media_tempo_team_b = str(self.team_b['Avg Duração'].iloc[0])

             # Kills
        media_kills_indiv_team_b = str(self.team_b['Avg Kills Indiv'].iloc[0])
        media_kills_sofridas_team_b = str(self.team_b['Avg Kills Sofridas'].iloc[0])
        media_kills_team_b = str(self.team_b['Avg Kills'].iloc[0])

            # Torres
        media_torres_indiv_team_b = str(self.team_b['Avg Towers Indiv'].iloc[0])
        media_torres_sofridas_team_b = str(self.team_b['Avg Towers Sofridas'].iloc[0])
        media_torres_team_b = str(self.team_b['Avg towers'].iloc[0])

            # Drakes
        media_drakes_indiv_team_b = str(self.team_b['Avg drakes Indiv'].iloc[0])
        media_drakes_sofridos_team_b = str(self.team_b['Avg drakes sofridos'].iloc[0])
        media_drakes_team_b = str(self.team_b['Avg drakes'].iloc[0])

            # Porcentagens
        percentages_over_11_5_torres_team_b = str(self.team_b['% Over 11,5 torres'].iloc[0])
        percentages_over_12_5_torres_team_b = str(self.team_b['% Over 12,5 torres'].iloc[0])

        percentages_over_4_5_drakes_team_b = str(self.team_b['% Over 4,5 drakes'].iloc[0])
        percentages_over_5_5_drakes_team_b = str(self.team_b['% Over 5,5 drakes'].iloc[0])

        percentages_over_kill_escolhido_team_b = str(self.team_b[f'% Over {kill_escolhida}'].iloc[0])

        percentages_over_27_30_mins_team_b = str(self.team_b['% Under 27:30'].iloc[0])
        percentages_over_27_30_mins_team_b = (str(100 - float(percentages_over_27_30_mins_team_b.rstrip('%')))+'%').replace('.0', '')

        percentages_over_28_30_mins_team_b = str(self.team_b['% Under 28:30'].iloc[0])
        percentages_over_28_30_mins_team_b = (str(100 - float(percentages_over_28_30_mins_team_b.rstrip('%')))+'%').replace('.0', '')

        percentages_over_29_30_mins_team_b = str(self.team_b['% Under 29:30'].iloc[0])
        percentages_over_29_30_mins_team_b = (str(100 - float(percentages_over_29_30_mins_team_b.rstrip('%')))+'%').replace('.0', '')

        percentages_over_30_30_mins_team_b = str(self.team_b['% Under 30:30'].iloc[0])
        percentages_over_30_30_mins_team_b = (str(100 - float(percentages_over_30_30_mins_team_b.rstrip('%')))+'%').replace('.0', '')

        percentages_over_31_30_mins_team_b = str(self.team_b['% Under 31:30'].iloc[0])
        percentages_over_31_30_mins_team_b = (str(100 - float(percentages_over_31_30_mins_team_b.rstrip('%')))+'%').replace('.0', '')

        percentages_over_32_30_mins_team_b = str(self.team_b['% Under 32:30'].iloc[0])
        percentages_over_32_30_mins_team_b = (str(100 - float(percentages_over_32_30_mins_team_b.rstrip('%')))+'%').replace('.0', '')

        percentages_over_33_30_mins_team_b = str(self.team_b['% Under 33:30'].iloc[0])
        percentages_over_33_30_mins_team_b = (str(100 - float(percentages_over_33_30_mins_team_b.rstrip('%')))+'%').replace('.0', '')

        percentages_over_34_30_mins_team_b = str(self.team_b['% Under 34:30'].iloc[0])
        percentages_over_34_30_mins_team_b = (str(100 - float(percentages_over_34_30_mins_team_b.rstrip('%')))+'%').replace('.0', '')



        ### Expectativas de cada time no confronto perante as estatisticas individuais
        expec_kills_team_a_confronto = (float(media_kills_indiv_team_a) + float(media_kills_sofridas_team_b)) / 2
        expec_kills_team_b_confronto = (float(media_kills_indiv_team_b) + float(media_kills_sofridas_team_a)) / 2

        expec_drakes_team_a_confronto = (float(media_drakes_indiv_team_a) + float(media_drakes_sofridos_team_b)) / 2
        expec_drakes_team_b_confronto = (float(media_drakes_indiv_team_b) + float(media_drakes_sofridos_team_a)) / 2

        excep_torres_team_a_confronto = (float(media_torres_indiv_team_a) + float(media_torres_sofridas_team_b)) / 2
        excep_torres_team_b_confronto = (float(media_torres_indiv_team_b) + float(media_torres_sofridas_team_a)) / 2 

        ### XG confronto
        xg_kills = expec_kills_team_a_confronto + expec_kills_team_b_confronto
        xg_drakes = expec_drakes_team_a_confronto + expec_drakes_team_b_confronto
        xg_torres = excep_torres_team_a_confronto + excep_torres_team_b_confronto


        ### Poisson - probabilidades - prognóstico
            # Drakes
        over_45_prob = 0
        for k in range(5, 1000):
            over_45_prob += poisson.pmf(k, xg_drakes)
        over_45_percent = round(over_45_prob * 100, 2)
        odd_4_5 = round(1 / over_45_prob, 2)
        #print(f"A odd de Over 4.5 Drakes: {odd_45:.2f}")

        over_55_prob = 0
        for k in range(6, 1000):
            over_55_prob += poisson.pmf(k, xg_drakes)
        over_55_percent = round(over_55_prob * 100, 2)
        odd_5_5 = round(1 / over_55_prob, 2)
        #print(f"\nProbabilidade de Over 4.5 Drakes: {over_55_percent:.2f}%")

            # Torres
        over_11_5_prob = 0
        for k in range(12, 1000):
            over_11_5_prob += poisson.pmf(k, xg_torres)
        over_11_5_percent = round(over_11_5_prob * 100, 2)
        odd_11_5 = round(1 / over_11_5_prob, 2)
        #print(f"\nProbabilidade de Over 11.5 Torres: {over_11_5_percent:.2f}%")

        over_12_5_prob = 0
        for k in range(13, 1000):
            over_12_5_prob += poisson.pmf(k, xg_torres)
        over_12_5_percent = round(over_12_5_prob * 100, 2)
        odd_12_5 = round(1 / over_12_5_prob, 2)
        #print(f"\nProbabilidade de Over 12.5 Torres: {over_12_5_percent:.2f}%")



            # Kills
        tratamento_kill_escolhida = kill_escolhida.replace(',5', '')
        tratamento_kill_escolhida = int(tratamento_kill_escolhida)
        tratamento_kill_escolhida = tratamento_kill_escolhida + 1
        over_kill_escolhida = 0
        for k in range(tratamento_kill_escolhida, 1000):
            over_kill_escolhida += poisson.pmf(k, xg_kills)
        over_kill_escolhida_percent = round(over_kill_escolhida * 100, 2)
        odd_kill_escolhida = round(1 / over_kill_escolhida, 2)
        #print(f"\nProbabilidade de Over {kill_escolhida} kills: {over_kill_escolhida_percent:.2f}%")


        

        ### Layout 2 -> Stats e prognostico do confronto em poisson
        over_drakes = {
            'Over 4,5': over_45_percent,
            'Over 5,5': over_55_percent
        }
        # Configurar os dados do gráfico
        labels = list(over_drakes.keys())
        values = list(over_drakes.values())
        colors = ['lightblue', 'lightgreen', 'orange', 'pink']
        # Configurar a fonte
        fonte = {'fontname': 'Arial'}
        # Criar o gráfico de colunas
        fig, ax = plt.subplots(figsize=(4, 3))
        x = np.arange(len(labels))
        ax.bar(x, values, color=colors, edgecolor='black', width=0.2, ls='dashed', hatch='/', alpha=0.5)
        # Configurar os rótulos do eixo x
        ax.set_xticks(x)
        ax.set_xticklabels(labels, **fonte)
        # Adicionar os valores acima das colunas
        # for i, v in enumerate(values):
        #    ax.text(i, v, str(v), ha='center', va='bottom', **fonte)
        # Adicionar o título do gráfico
        ax.set_title('% Over drakes', fontsize=11, fontstyle='italic', fontweight='bold', **fonte)

        sg.theme('GreenTan')

        grafico_dos_over = 'grafico.png'
        plt.savefig(grafico_dos_over)

        # Layout da janela
        layout_um = [
        [sg.Text(f'{home}:', font=('Calibri', 13, 'bold'), justification='center')],
        [sg.HorizontalSeparator()],
        [sg.Text(f'Estatisticas do time', font=('Calibri', 12, 'italic', 'bold'), justification='center')],
        [sg.Text('Avg kills indiv: ', font=('Calibri', 11, 'italic')),
         sg.Text(media_kills_indiv_team_a, font=('Calibri', 11))],
        [sg.Text('Avg kills sofridas', font=('Calibri', 11, 'italic')),
         sg.Text(media_kills_sofridas_team_a, font=('Calibri', 11))],
        [sg.Text('Avg drakes feitos:', font=('Calibri', 11, 'italic')),
         sg.Text(media_drakes_indiv_team_a, font=('Calibri', 11))],
        [sg.Text('Avg drakes sofridos:', font=('Calibri', 11, 'italic')),
         sg.Text(media_drakes_sofridos_team_a, font=('Calibri', 11))],
        [sg.Text('Avg torres indiv:', font=('Calibri', 11, 'italic')),
         sg.Text(media_torres_indiv_team_a, font=('Calibri', 11))],
        [sg.Text('Avg torres sofridas:', font=('Calibri', 11, 'italic')),
         sg.Text(media_torres_sofridas_team_a, font=('Calibri', 11))]
        ]

        layout_dois = [
        [sg.Text(f'{away}:', font=('Calibri', 13, 'bold'), justification='center')],
        [sg.HorizontalSeparator()],
        [sg.Text(f'Estatisticas do time', font=('Calibri', 12, 'italic', 'bold'), justification='center')],
        [sg.Text('Avg kills indiv: ', font=('Calibri', 11, 'italic')),
         sg.Text(media_kills_indiv_team_b, font=('Calibri', 11))],
        [sg.Text('Avg kills sofridas', font=('Calibri', 11, 'italic')),
         sg.Text(media_kills_sofridas_team_b, font=('Calibri', 11))],
        [sg.Text('Avg drakes feitos:', font=('Calibri', 11, 'italic')),
         sg.Text(media_drakes_indiv_team_b, font=('Calibri', 11))],
        [sg.Text('Avg drakes sofridos:', font=('Calibri', 11, 'italic')),
         sg.Text(media_drakes_sofridos_team_b, font=('Calibri', 11))],
        [sg.Text('Avg torres indiv:', font=('Calibri', 11, 'italic')),
         sg.Text(media_torres_indiv_team_b, font=('Calibri', 11))],
        [sg.Text('Avg torres sofridas:', font=('Calibri', 11, 'italic')),
         sg.Text(media_torres_sofridas_team_b, font=('Calibri', 11))]
        ]

        layout_tres = [
        [sg.Text(f'Stats do Confronto:', font=('Calibri', 12, 'bold'), justification='center')],
        [sg.HorizontalSeparator()],
        [sg.Text(f'Expectativa do confronto', font=('Calibri', 12, 'italic', 'bold'), justification='center')],
        [sg.Text('xG Kills:', font=('Calibri', 12, 'italic')), sg.Text(xg_kills, font=('Calibri', 11))],
        [sg.Text('xG Drakes', font=('Calibri', 12, 'italic')), sg.Text(xg_drakes, font=('Calibri', 11))],
        [sg.Text('xG Torres:', font=('Calibri', 12, 'italic')), sg.Text(xg_torres, font=('Calibri', 11))],
        [sg.Text(f'Probabilidades - Poisson', font=('Calibri', 12, 'italic', 'bold'), justification='center')],
        [sg.Text('% Over 11,5 torres:', font=('Calibri', 11, 'italic')), sg.Text(over_11_5_percent, font=('Calibri', 11)),
         sg.Text('-', font=('Calibri', 11)), sg.Text(odd_11_5, font=('Calibri', 11))],
        [sg.Text('% Over 12, 5 torres:', font=('Calibri', 11, 'italic')), sg.Text(over_12_5_percent, font=('Calibri', 11)),
         sg.Text('-', font=('Calibri', 11)), sg.Text(odd_12_5, font=('Calibri', 11))],
         [sg.Text(f'% Over {kill_escolhida} kills:', font=('Calibri', 11, 'italic')), sg.Text(over_kill_escolhida_percent, font=('Calibri', 11)),
         sg.Text('-', font=('Calibri', 11)), sg.Text(odd_kill_escolhida, font=('Calibri', 11))]
        ]


        layout_quatro = [
        [sg.Image(grafico_dos_over, size=(460, 320))],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Text(odd_4_5, font=('Calibri', 12, 'italic')), sg.Push(),
         sg.Text(odd_5_5, font=('Calibri', 12)),
         sg.Push()]
        ]

        layout_stats = [
            [sg.Column(layout_um), sg.VSeparator(), sg.Column(layout_dois), sg.VSeparator(), sg.Column(layout_tres), sg.VSeparator(),  sg.Column(layout_quatro),
            ]
        ]
        window = sg.Window(f'Stats do Confronto: {home} x {away}', layout_stats,
                        icon='C:/Users/Joao Luiz/Documents/icons/video-game-controller.ico')
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            else:
                pass

        window.close()








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
        
        self.ligas = self.connection.return_ligas()['Liga']

        self.ligas = self.ligas.sort_values().reset_index(drop=True)

        self.base_iteracao = self.connection.base_iteracao()

        #print(f"\n{self.base_iteracao}")
        #print(f'Type of self.ligas: {type(self.ligas)}')
        #print(f'self.ligas: {self.ligas}')

        for camp in self.ligas:
            #rint(f'\nCamp: {camp}')
            #print(self.base_iteracao['Liga'].unique())  # Verifique os valores únicos na coluna 'Liga'
            #print(self.base_iteracao[self.base_iteracao['Liga'].str.strip().str.upper() == camp.strip().upper()])
            #print(self.base_iteracao.loc[self.base_iteracao['Liga'].str.strip().str.upper() == camp.strip().upper(), 'Time'].unique())
            list_teams = list(set(self.base_iteracao.loc[self.base_iteracao['Liga'] == f'{camp}', 'Time'].unique()))
            self.lista_ligas[camp] = list_teams


        #self.lista_ligas = self.ligas["Liga"].to_list() 
        #print(type(self.lista_ligas))
        #print(f"\n{self.lista_ligas}")

        sg.theme('GreenTan')
        layout_left = [
            [sg.Image(filename='C:/Users/Joao Luiz/Documents/icons/teste.png', size=(400, 266))]
        ]
        layout_right = [
            [sg.Text('Escolha uma liga:', font=('Calibri', 12, 'italic', 'bold'))], [sg.Combo(list(self.lista_ligas.keys()), key='-LIGA-', font=('Calibri', 11), enable_events=True, size=(20, 1))],
            [sg.Text('Escolha o time A:', font=('Calibri', 12, 'italic', 'bold'))], [sg.Combo([], key='-TIME_A-', font=('Calibri', 11), enable_events=True, size=(20, 1))],
            [sg.Text('Escolha o time B:', font=('Calibri', 12, 'italic', 'bold'))], [sg.Combo([], key='-TIME_B-', font=('Calibri', 11), enable_events=True, size=(20, 1))],
            [sg.Text('Escolha a qtd de kills:', font=('Calibri', 12, 'italic', 'bold'))], [sg.Combo(LISTA_KILLS, key='-KILLS-', font=('Calibri', 11), enable_events=True, size=(20, 1))],
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
                kill = values['-KILLS-']
                self.validar_selecao(liga, time_a, time_b, kill)

            elif event == '-EXPORTAR-':
                # Extrair a tabela de confrontos escolhidos no BD depois de fechar a interface gráfica
                pass

            elif event == '-LIGA-':
                times = self.lista_ligas[values['-LIGA-']]
                window['-TIME_A-'].update(values=times)
                window['-TIME_B-'].update(values=times)

            elif event == '-TIME_A-' or event == '-TIME_B-':
                time_a = values['-TIME_A-']
                time_b = values['-TIME_B-']
                kill = values['-KILLS-']
                if time_a == time_b:
                    self.validar_selecao(None, time_a, time_b, kill)

            elif event == '-ATUALIZAR-':
                # Atualizar o layout
                window['-LIGA-'].update("")
                window['-TIME_A-'].update("")
                window['-TIME_B-'].update("")
                window['-KILLS-'].update("")
                # ...
                pass

        window.close()

def main():

    executar_layout = Projeto()

    executar_layout.mostrar_layout_principal(executar_layout.layout_principal())




main()