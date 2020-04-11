import java.util.*;

public class BFS {

    BFS(){

    }

    public State breadthFirstSearch(Grid grid){
        State initialState = new State(grid, grid.getStart());
        // int[] position = initialState.getPosition();
        int visitedStates[][] = new int[grid.getNumOfRows()][grid.getNumOfColumns()];

        Stack<State> stack = new Stack<>();
        stack.add(initialState);

        while (!stack.isEmpty()){

            State state = stack.pop(); 
            ArrayList<State> children = state.successorStates();
            
            if (state.goalReached())
                return state;


                while (!children.isEmpty()){
                    State child = children.get(children.size()-1);
                    if (!child.isVisited(visitedStates)){
                        stack.add(child);
                        System.out.println("child\n");
                    }
                    children.remove(child); 
            }
        }
        return null;
    }

}