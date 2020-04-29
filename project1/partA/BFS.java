import java.util.*;

public class BFS {

    BFS(){

    }

    public State breadthFirstSearch(Grid grid){
        State initialState = new State(grid, grid.getStart());
        int visitedStates[][] = new int[grid.getNumOfRows()][grid.getNumOfColumns()];

        Queue<State> queue = new LinkedList<>();
        queue.add(initialState);
        int statesExpandedCount = 0;

        while (!queue.isEmpty()){

            State state = queue.remove(); 
            ArrayList<State> children = state.successorStates(false);
            statesExpandedCount++;
            if (state.goalReached())
            {
                System.out.println("Expanded states count: " + statesExpandedCount);
                return state;
            }

                while (!children.isEmpty()){
                    State child = children.get(children.size()-1);
                    if (!child.isVisited(visitedStates)){
                        queue.add(child);
                    }
                    children.remove(child); 
                }
        }
        return null;
    }

}