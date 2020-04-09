import java.util.ArrayList; 

public class State {

    private int [] position;
    private State parentNode;
    private Grid grid;
    private int numOfRows;
    private int numOfColumns;  

   

    State(Grid grid, int[] position) {

        this.position = position;
        this.grid = grid; 
        this.numOfRows = grid.getNumOfRows();
        this.numOfColumns = grid.getNumOfColumns();
    }

    public boolean isLegal(){
        if (this.position[0] >= 0 && this.position[0] <= numOfRows && 
            this.position[1] >= 0 && this.position[1] <= numOfColumns)
            {
                return true; 
            }
        return false;     
    }

    public ArrayList<State> successorStates(){

        ArrayList<State> childNodes = new ArrayList<State>();
        
        // Move Right. 
        int[] newPosition = new int[2]; 
        newPosition[0] = position[0] + 1;
        newPosition[1] = position[1];

        State newState = new State(this.grid, newPosition);  
        if (newState.isLegal())
        {
            newState.parentNode = this;
            childNodes.add(newState);
            System.out.println("Child State."+newState.position[0]+"\n"); 
        }

        // Move Left.  
        newPosition[0] = position[0] -1;
        newPosition[1] = position[1];

        newState = new State(this.grid, newPosition);  
        if (newState.isLegal())
        {
            newState.parentNode = this;
            childNodes.add(newState);
            System.out.println("Child State."+newState.position[0]+"\n"); 
        }

        // Move Up.  
        newPosition[0] = position[0];
        newPosition[1] = position[1]+1;

        newState = new State(this.grid, newPosition);  
        if (newState.isLegal())
        {
            newState.parentNode = this;
            childNodes.add(newState);
            System.out.println("Child State."+newState.position[1]+"\n"); 
        }

        // Move Down.  
        newPosition[0] = position[0];
        newPosition[1] = position[1]-1;

        newState = new State(this.grid, newPosition);  
        if (newState.isLegal())
        {
            newState.parentNode = this;
            childNodes.add(newState);
            System.out.println("Child State."+newState.position[1]+"\n"); 
        }
        return childNodes; 
    }

    public boolean isVisited(int[][] visitedStates){
        if (visitedStates[this.position[0]][this.position[1]] == 1){
            return true; 
        } 
        visitedStates[this.position[0]][this.position[1]] = 1; 
        return false; 
    }

    public int[] getPosition(){
        return this.position; 
    }
}