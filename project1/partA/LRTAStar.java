import java.util.*;

public class LRTAStar {
    LRTAStar() { }

    public State LRTAStarSearch(Grid grid) {
        State s = null;
        State a = null;

        HashMap<Cell, Double> H = new HashMap<Cell, Double>();
        HashMap<Cell, State> S = new HashMap<Cell, State>();
        State sPrime = new State(grid, grid.getStart());

        int count = 1;
        while (true) {
            if (sPrime.goalReached()) {
                return S.get(sPrime.getParentNode().getCell());
            }
            else {
                if (!H.containsKey(sPrime.getCell())) {
                    H.put(sPrime.getCell(), sPrime.findH());
                    S.put(sPrime.getCell(), sPrime);
                }
                
                if (s != null) {
                    double min = Double.MAX_VALUE;
                    State sMin = null;
                    for (State state : s.successorStates(false)) {
                        double cost = LRTACost(s, state, H);
                        if (cost < min) {
                            min = cost;
                            sMin = state;
                        }
                    }
                    H.put(s.getCell(), min);
                    S.put(s.getCell(), sMin);
                }

                double min = Double.MAX_VALUE;
                for (State state : sPrime.successorStates(true)) {
                    double cost = LRTACost(sPrime, state, H);
                    if (cost < min) {
                        min = cost;
                        a = state;
                    }
                }
            }

            s = sPrime;
            sPrime = a;
            count++;
        }
    }

    public double LRTACost(State s, State sPrime, HashMap<Cell, Double> H) {
        if (!H.containsKey(sPrime.getCell())) {
            return s.findH();
        }
        return s.getG() + H.get(sPrime.getCell());
    }
}