from dataclasses import dataclass

import requests

from statusinvest.auth import Auth
from statusinvest.base import STATUS_INVEST_BASE_URL

INDICATORS_URL = '/indicatorhistoricallist'


@dataclass
class Indicator:
    actual: float
    avg: float


class StockTicker:
    def __init__(self, *args, **kwargs) -> None:
        self.dy = Indicator(*kwargs.get('dy').values())
        self.p_l = Indicator(*kwargs.get('p_l').values())
        self.p_vp = Indicator(*kwargs.get('p_vp').values())
        self.p_ebita = Indicator(*kwargs.get('p_ebita').values())
        self.p_ebit = Indicator(*kwargs.get('p_ebit').values())
        self.p_sr = Indicator(*kwargs.get('p_sr').values())
        self.p_ativo = Indicator(*kwargs.get('p_ativo').values())
        self.p_capitlgiro = Indicator(*kwargs.get('p_capitlgiro').values())
        self.p_ativocirculante = Indicator(
            *kwargs.get('p_ativocirculante').values())
        self.peg_Ratio = Indicator(*kwargs.get('peg_Ratio').values())
        self.dividaliquida_patrimonioliquido = Indicator(
            *kwargs.get('dividaliquida_patrimonioliquido').values())
        self.dividaliquida_ebitda = Indicator(
            *kwargs.get('dividaliquida_ebitda').values())
        self.dividaliquida_ebit = Indicator(
            *kwargs.get('dividaliquida_ebit').values())
        self.patrimonio_ativo = Indicator(
            *kwargs.get('patrimonio_ativo').values())
        self.passivo_ativo = Indicator(*kwargs.get('passivo_ativo').values())
        self.liquidezcorrente = Indicator(
            *kwargs.get('liquidezcorrente').values())
        self.margembruta = Indicator(*kwargs.get('margembruta').values())
        self.margemebitda = Indicator(*kwargs.get('margemebitda').values())
        self.margemebit = Indicator(*kwargs.get('margemebit').values())
        self.margemliquida = Indicator(*kwargs.get('margemliquida').values())
        self.roe = Indicator(*kwargs.get('roe').values())
        self.roa = Indicator(*kwargs.get('roa').values())
        self.roic = Indicator(*kwargs.get('roic').values())
        self.giro_ativos = Indicator(*kwargs.get('giro_ativos').values())
        self.ev_ebitda = Indicator(*kwargs.get('ev_ebitda').values())
        self.ev_ebit = Indicator(*kwargs.get('ev_ebit').values())
        self.lpa = Indicator(*kwargs.get('lpa').values())
        self.vpa = Indicator(*kwargs.get('vpa').values())
        self.receitas_cagr5 = Indicator(*kwargs.get('receitas_cagr5').values())
        self.lucros_cagr5 = Indicator(*kwargs.get('lucros_cagr5').values())

    @staticmethod
    def new(ticker: str, category: str):
        ticker = ticker.lower()

        response = requests.post(
            url=f'{STATUS_INVEST_BASE_URL}/{category}{INDICATORS_URL}',
            headers=Auth.from_env().auth_headers,
            data={
                'codes[]': ticker,
                'time': 5,
                'byQuarter': False,
                'futureData': False,
            }
        )

        data = response.json()
        indicators = dict(map(lambda x: (
            x['key'], {'actual': x['actual'], 'avg': x['avg']}), data['data'][ticker])
        )

        return StockTicker(**indicators)
