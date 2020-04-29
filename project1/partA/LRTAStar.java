import java.util.*;

public class LRTAStar {
    LRTAStar() { }

    public State LRTAStarSearch(Grid grid) {
        State s = null;
        State a = null;

        HashMap<Cell, Double> H = new HashMap<Cell, Double>();
        State sPrime = new State(grid, grid.getStart());

        while (true) {
            if (sPrime.goalReached()) {
                return sPrime.getParentNode();
            }
            else {
                if (!H.containsKey(sPrime.getCell())) {
                    H.put(sPrime.getCell(), sPrime.findH());
                }
                
                if (s != null) {
                    double min = Double.MAX_VALUE;
                    for (State state : s.successorStates(false)) {
                        if(!H.containsKey(state.getCell()))
                            continue;

                        double cost = LRTACost(state, s, H);
                        if (cost < min) {
                            min = cost;
                        }
                    }
                    H.put(s.getCell(), min);
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
        }
    }

    public double LRTACost(State s, State sPrime, HashMap<Cell, Double> H) {
        if (!H.containsKey(sPrime.getCell())) {
            return sPrime.findH();
        }
        return s.getG() + H.get(sPrime.getCell());
    }
}