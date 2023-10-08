import React from 'react';

function Job(props) {
    function download_data() {
        try {
          fetch("http://127.0.0.1:8000/api/mongo_crawljobs?id="+props.id, {
            method: "GET",
            headers: {
                "Accept":"application/json",
                "Content-Type": "application/json",
            },
          })
            .then((respnose) => respnose.json())
            .then(data => {
                var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data,undefined,4));
                var downloadAnchorNode = document.createElement('a');
                downloadAnchorNode.setAttribute("href",     dataStr);
                downloadAnchorNode.setAttribute("download", props.id + ".json");
                document.body.appendChild(downloadAnchorNode);
                downloadAnchorNode.click();
                downloadAnchorNode.remove();
                })
        } catch (error) {
          console.log(error);
        }
      }

    function re_run_job() {
        try {
            fetch("http://127.0.0.1:8000/api/crawler?re_id="+props.id, {
              method: "POST",
              headers: {
                  "Accept":"application/json",
                  "Content-Type": "application/json",
              },
            })
              .then((respnose) => respnose)
              setTimeout(() => {
                window.location.reload();
              }, 500);
          } catch (error) {
            console.log(error);
          }
    }

    function delete_job() {
      if (window.confirm('Are you sure you wish to delete this job?')) {
        try {
          fetch("http://127.0.0.1:8000/api/crawler", {
            method: "DELETE",
            headers: {
                "Accept":"application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
              "id": props.id,
            }),
          })
            .then((respnose) => respnose)
            setTimeout(() => {
              window.location.reload();
            }, 500);
        } catch (error) {
          console.log(error);
        }
    }}

      return (
        <>
        <div className="col-md-4 text-bg-primary" style={{paddingBottom: "10px", margin: "10px"}}>
          <p><b>Job Name: </b>{props.name}</p>
          <p><b>Job Id:</b> {props.id}</p>
          <p><b>Creation Date:</b> {props.date}</p>
          <p><b>Job Status:</b> {props.status}</p>
          <div className="btn-group">
            {props.status === "done" &&
            <>
            <button className="btn btn-outline-light" onClick={download_data}>Download</button>
            <button className="btn btn-outline-light" onClick={delete_job}>Delete</button>
            </>
            }
            <button className="btn btn-outline-light" onClick={re_run_job}>Re-run as new task</button>
          </div>
        </div>
        </>
      );
}

class JobsList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            items: [],
            DataisLoaded: false,
            input_data: "",
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    };

    componentDidMount() {
        fetch("http://127.0.0.1:8000/api/crawler", {
        method: "GET",
        headers: {
            "Accept":"application/json",
            "Content-Type": "application/json",
        },
        })
        .then((response) => response.json())
        .then((json) => {
            this.setState({
                items: json,
                DataisLoaded: true
            });
        })
    }

    handleChange(event) {
      const fileReader = new FileReader();
      fileReader.onload = (event) => {
        this.setState({input_data: event.target.result})
      }
      fileReader.readAsText(event.target.files[0], "UTF-8");
    }

    handleSubmit(event) {
      event.preventDefault();
      try {
        fetch("http://127.0.0.1:8000/api/crawler", {
          method: "POST",
          headers: {
              "Accept":"application/json",
              "Content-Type": "application/json",
          },
          body: this.state.input_data
          })
          .then((response) => response.json())
          setTimeout(() => {
            window.location.reload();
          }, 500);
        } catch (error) {
          console.log(error);
        }
    }

    download_template(event) {
      event.preventDefault();
      const input_json = {
        "name": "",
        "url": [],
        "crawling_rules": [
          {
              "content_tag": "h1",
              "tag_attr": {
                  "class": ""
              }
          },
          {
              "content_tag": "div",
              "tag_attr": {
                  "id": ""
              }
          }
      ]
      };
      try {
          var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(input_json,undefined,4));
          var downloadAnchorNode = document.createElement('a');
              downloadAnchorNode.setAttribute("href", dataStr);
              downloadAnchorNode.setAttribute("download", "input_template.json");
              document.body.appendChild(downloadAnchorNode);
              downloadAnchorNode.click();
              downloadAnchorNode.remove();
      } catch (error) {
        console.log(error);
      }
    }

    render () {
        if (!this.state.DataisLoaded) return <> <h1> Loading.... </h1> </>;
        return (
        <>
        <div className="container">
        <br/>
        <div className="row justify-content-center">
        <div className="card col-md-4" style={{padding: "10px"}}>
        <h2>Upload job input JSON file</h2>
        <form onSubmit={this.handleSubmit}>
          <input className="btn btn-primary" type="submit" value="Submit"/>
          <input type="file" onChange={this.handleChange} style={{marginLeft: "10px"}}/>
          <br/>
          <a href="/#" onClick={this.download_template}>Download Template</a>
        </form>
        </div>
        <h2>Job List</h2>
            {this.state.items.map((item) => ( 
                <Job name= {item.name} id={item.job_ID} date={item.created} status={item.status}/>
                ))
            }
        </div>
        </div>
        </>)
        };
};
export default JobsList;