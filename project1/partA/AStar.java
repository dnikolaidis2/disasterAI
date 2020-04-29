import java.util.*;

public class AStar {

    AStar(){

    }

    public State aStarSearch(Grid grid){

        List<State> openList = new LinkedList<State>();
        List<State> closedList = new LinkedList<State>();

        State initialState = new State(grid, grid.getStart());
        initialState.generateF();
        openList.add(initialState);

        int statesExpandedCount = 0;

        while (!openList.isEmpty()){
            
            State cheapState = findMin(openList);
            openList.remove(cheapState);  
             
            
            ArrayList<State> children = cheapState.successorStates(false);
            statesExpandedCount++;
            while (!children.isEmpty()){
                State child = children.get(children.size()-1);
                
                if (child.goalReached())
                {
                    System.out.println("Expanded states count: " + statesExpandedCount);
                    return child;
                }
                
                // If i.e. a child lands on [3,4] and it's cost is more expensive than an
                // already expanded node on [3,4] then we don't expand the child. 
                State StateInSamePositionOpen = findCheaperState(openList, child.getPosition());
                if (StateInSamePositionOpen != null){
                    if (child.getF() > StateInSamePositionOpen.getF()){
                        children.remove(child);
                        continue;
                    } 
                }

                State StateInSamePositionClosed = findCheaperState(closedList, child.getPosition());
                if (StateInSamePositionClosed != null){    
                    if (child.getF() > StateInSamePositionClosed.getF()){
                        children.remove(child);
                        continue; 
                    }
                }
                openList.add(child);
                children.remove(child);
                

            }
            closedList.add(cheapState);
        }
        
        return null;
    }

    public State findMin(List<State> list){
        
        // check list is empty or not 
        if (list == null || list.size() == 0) { 
            return null; 
        } 
    
        State minState = list.get(0);
        for (int i=0; i < list.size(); i++){
            if (list.get(i).getF() < minState.getF())
                minState = list.get(i); 
        }
        return minState; 



    }

    public State findCheaperState(List<State> list, int[] position){
        
        List<State> StatesInPosition = new LinkedList<State>(); 
        // check list is empty or not 
        if (list == null || list.size() == 0) { 
            return null; 
        } 
    
        for (int i=0; i < list.size(); i++){
            if ((list.get(i).getPosition()[0] == position[0]) && (list.get(i).getPosition()[1] == position[1])){
                StatesInPosition.add(list.get(i)); 
            }
        }
        if (StatesInPosition.isEmpty())
            return null; 
        else 
            return findMin(StatesInPosition); 
    }
}