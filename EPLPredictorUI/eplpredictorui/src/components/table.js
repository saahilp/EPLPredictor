import React from 'react'
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import './table.css';

class LeagueTable extends React.Component {

    constructor(props) {
        super(props);
        this.state = {table: []}
    }

    render() {

        console.log(this.state.table);
        return (
        <TableContainer component={Paper}>
        <Table stickyHeader style={{minWidth: 650, maxHeight: 400}}>
          <TableHead>
            <TableRow>
            <TableCell align="right">Position</TableCell>
              <TableCell align="left">Team</TableCell>
              <TableCell align="right">Played</TableCell>
              <TableCell align="right">Wins</TableCell>
              <TableCell align="right">Draws</TableCell>
              <TableCell align="right">Losses</TableCell>
              
              <TableCell align="right">Goals Scored</TableCell>
              <TableCell align="right">Goals Conceded</TableCell>
              <TableCell align="right">Goal Difference</TableCell>
              <TableCell align="right">Points</TableCell>
            </TableRow>
          </TableHead>
          <TableBody className="rows">
            {this.state.table.map((row, index) => (
              <TableRow  key = {row.name} >
                <TableCell align="right">{index+1}</TableCell>
                <TableCell align="left">{row.name}</TableCell>
                <TableCell align="right">38</TableCell>
                <TableCell align="right">{row.wins}</TableCell>
                <TableCell align="right">{row.draws}</TableCell>
                <TableCell align="right">{row.losses}</TableCell>
                
                <TableCell align="right">{row.goals_for}</TableCell>
                <TableCell align="right">{row.goals_conceded}</TableCell>
                <TableCell align="right">{row.goal_difference}</TableCell>
                <TableCell align="right">{row.points}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer> 
        )
    }

    

    componentDidMount() {
        fetch('http://127.0.0.1:5000/api/table')
            .then(res => res.json())
             .then(   (result) => {
                    this.setState({
                        table: result.table 
                    })
                    
                }
            )
    }
}

export default LeagueTable