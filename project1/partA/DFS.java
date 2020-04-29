import java.util.*;

public class DFS {

    DFS(){

    }

    public State depthFirstSearch(Grid grid){
        State initialState = new State(grid, grid.getStart());
        int visitedStates[][] = new int[grid.getNumOfRows()][grid.getNumOfColumns()];

        Stack<State> stack = new Stack<>();

        stack.push(initialState);
        int statesExpandedCount = 0;

        while (stack.empty() == false){

            State state = stack.pop();
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
                    stack.add(child);
                    
                }
                children.remove(child); 
            }
        }
        return null;         
    }
    
}