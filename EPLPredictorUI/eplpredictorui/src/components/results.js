import React from 'react';
import {NavigateNext, NavigateBefore} from '@material-ui/icons';
import './results.css'

class Results extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            results: [],
            dates: [],
            currDate: 0,
            resToShow: []
        }
    }

    render() {
        
        return (
            <div className="resultsPageContainer">
                <div className="headerContainer">
                    <div onClick={this.prevDate.bind(this)} className="headerComp" >
                        <NavigateBefore fontSize="large" />
                    </div>
                    <h3 className="headerComp">{this.state.dates[this.state.currDate]}</h3>
                    <div onClick ={this.nextDate.bind(this)} className="headerComp">
                        <NavigateNext fontSize="large"/>
                    </div>
                </div>

                <div className="resultsContainer">
                    {this.state.resToShow.map((row, index) => (
                        <p> {row[0]} <p className="resultsComp"> {row[1]} - {row[3]} </p> {row[2]} </p>
                    ))}
                </div>

            </div>
            
        )
    }

    componentDidMount() {
        fetch('http://127.0.0.1:5000/api/results')
            .then(res => res.json())
             .then(   (result) => {
                 
                    this.setState({
                        results: result.results,
                        currDate: 0 
                    }, () => {
                        var dates = this.state.dates;
                        this.state.results.forEach(function(item) {
                            if(!dates.includes(item[4]))
                                dates.push(item[4]);
                        })
                        this.setState({
                            dates: dates,
                            resToShow: this.state.results.filter((result) => {
                                return result[4] === this.state.dates[this.state.currDate]
                            })
                        })
                        console.log(this.state)
                    })
                    
                }
            )
    }

    prevDate() {
        if(this.state.currDate > 0) {
            this.setState ({
                currDate: this.state.currDate - 1
            }, () => {
                this.setState({
                    resToShow: this.state.results.filter((result) => {
                        return result[4] === this.state.dates[this.state.currDate]
                    })
                })
            })
        }
    }



    nextDate() {
        if(this.state.currDate < this.state.dates.length) {
            this.setState ({
                currDate: this.state.currDate + 1
            }, () => {
                this.setState({
                    resToShow: this.state.results.filter((result) => {
                        return result[4] === this.state.dates[this.state.currDate]
                    })
                })
            })
        }
    }

}

export default Results;