import java.util.*;

public class BFS {

    BFS(){

    }

    public State breadthFirstSearch(Grid grid){
        State initialState = new State(grid, grid.getStart());
        int visitedStates[][] = new int[grid.getNumOfRows()][grid.getNumOfColumns()];

        Queue<State> queue = new LinkedList<>(); //Is it though?
        queue.add(initialState);

        while (!queue.isEmpty()){

            State state = queue.remove(); 
            ArrayList<State> children = state.successorStates();
            
            if (state.goalReached())
                return state;


                while (!children.isEmpty()){
                    State child = children.get(children.size()-1);
                    if (!child.isVisited(visitedStates)){
                        queue.add(child);
                        System.out.println("child\n");
                    }
                    children.remove(child); 
            }
        }
        return null;
    }

}