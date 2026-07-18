from agents.market_agent import MarketAgent
from agents.strategy_agent import StrategyAgent
from agents.risk_agent import RiskAgent

from core.decision_engine import DecisionEngine



class SaiCore:


    def __init__(self):

        self.market = MarketAgent()

        self.strategy = StrategyAgent()

        self.risk = RiskAgent()

        self.decision = DecisionEngine()



    def think(self, data):


        market_view = (
            self.market
            .analyze(data)
        )


        strategy = (
            self.strategy
            .decide(market_view)
        )


        risk = (
            self.risk
            .evaluate(strategy)
        )


        final = (
            self.decision
            .decide(
                strategy,
                risk
            )
        )


        return {

            "market":market_view,

            "strategy":strategy,

            "risk":risk,

            "decision":final

        }