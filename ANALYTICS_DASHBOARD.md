# FRAMES Analytics Dashboard

## Overview

The **Program Analytics Dashboard** is a dynamic, flexible visualization tool that allows faculty and staff to explore relationships between different variables in their space program data. Unlike the network visualization (connection tracker), this dashboard focuses on **quantitative analysis** and **data relationships**.

## Key Features

### 1. **Dynamic Metric Selection**
Choose what you want to measure:
- **Student Count**: Total number of students
- **Average Terms to Graduation**: How long until students graduate
- **Student Status Distribution**: Breakdown by incoming/established/outgoing
- **Team Count**: Number of teams in your program
- **Faculty/Mentor Count**: Number of mentors and advisors
- **Project Count**: Number of active projects
- **Students by Status & Expertise**: Cross-tabulation showing students grouped by both status and expertise area

### 2. **Flexible Grouping (Dimensions)**
Group your data by different dimensions to see patterns:
- **University**: Compare across institutions
- **Project**: See how different projects compare
- **Team**: Analyze individual teams
- **Student Status**: incoming, established, outgoing
- **Expertise Area**: Software, Electrical, Mechanical, etc.
- **Team Discipline**: Engineering disciplines
- **Faculty Role**: PI, Co-PI, Advisors, etc.
- **Project Type**: CubeSat, PROVES, Research, etc.

### 3. **Multiple Visualization Types**
Choose the best way to view your data:
- **Bar Chart**: Great for comparing categories
- **Line Chart**: Good for trends (when time data is added)
- **Pie Chart**: Shows proportions of a whole
- **Doughnut Chart**: Like pie chart, more modern look
- **Radar Chart**: Compare multiple dimensions simultaneously

### 4. **Advanced Filtering**
Filter your analysis by:
- University
- Project
- Team
- Student status
- Expertise area
- Faculty role

### 5. **Auto-Generated Insights**
The dashboard automatically calculates:
- Total values
- Highest and lowest categories
- Averages
- Distribution patterns

## How People Understand Data

The dashboard is designed based on cognitive science principles:

### **Comparison** (Bar/Column Charts)
- **Best for**: Comparing discrete categories
- **Example**: "How many students does each university have?"
- **Use when**: You want to see which category is highest/lowest

### **Part-to-Whole** (Pie/Doughnut Charts)
- **Best for**: Understanding proportions
- **Example**: "What percentage of students are incoming vs. established?"
- **Use when**: You want to see how parts make up a whole

### **Correlation** (Scatter - future)
- **Best for**: Seeing relationships between two continuous variables
- **Example**: "Does team size correlate with project success?"
- **Use when**: You want to find patterns between variables

### **Distribution** (future enhancement)
- **Best for**: Understanding how data is spread
- **Example**: "How are students distributed across expertise areas?"
- **Use when**: You want to see frequency and range

## Example Use Cases

### Use Case 1: Understanding Student Pipeline
**Question**: "How healthy is our student pipeline?"

**Steps**:
1. Select metric: "Student Status Distribution"
2. Filter by: Your university
3. Visualization: Doughnut chart
4. **Insight**: If you have too many "outgoing" students and few "incoming", you have a pipeline problem

### Use Case 2: Comparing Team Sizes Across Projects
**Question**: "Which projects have the most teams?"

**Steps**:
1. Select metric: "Team Count"
2. Group by: "Project"
3. Filter by: Your university (or leave blank for all)
4. Visualization: Bar chart
5. **Insight**: See which projects are most/least staffed

### Use Case 3: Faculty Distribution
**Question**: "What types of mentors do we have?"

**Steps**:
1. Select metric: "Faculty/Mentor Count"
2. Group by: "Faculty Role"
3. Visualization: Bar chart
4. **Insight**: Identify gaps in mentorship (e.g., not enough industry mentors)

### Use Case 4: Cross-Analysis
**Question**: "How are students distributed across expertise areas and status?"

**Steps**:
1. Select metric: "Students by Status & Expertise"
2. Filter by: Your university
3. Visualization: Grouped bar chart
4. **Insight**: Find gaps (e.g., no incoming software engineers) or strengths

## Future Enhancements

The analytics system is designed to be extensible for future data sources:

### **Discord Integration** (Future)
- Message activity by team
- Active vs. inactive members
- Communication patterns over time

### **Project Management Tool Integration** (Future)
- Task completion rates
- Milestone tracking
- Burndown charts
- Team velocity

### **Time-Series Analysis** (Future)
- Student counts over academic terms
- Graduation rates by cohort
- Project completion trends
- Knowledge retention metrics

### **Predictive Analytics** (Future)
- Predict student graduation
- Forecast team turnover
- Identify at-risk projects
- Knowledge loss predictions

## Technical Details

### API Endpoints

**GET /api/analytics/dimensions**
- Returns available metrics, dimensions, and filters

**POST /api/analytics/data**
```json
{
  "metric": "student_count",
  "groupBy": "university",
  "filters": {
    "university_id": "CalPolyPomona",
    "status": "established"
  }
}
```

Returns aggregated data ready for visualization.

### Adding New Metrics

To add a new metric:

1. **Backend**: Add handler in `app.py` under `/api/analytics/data`
2. **Backend**: Add metric definition in `/api/analytics/dimensions`
3. **Frontend**: The UI will automatically pick it up

Example:
```python
elif metric == 'projects_by_duration':
    query = db.session.query(
        ProjectModel.duration,
        func.count(ProjectModel.id).label('count')
    ).group_by(ProjectModel.duration)
    results = query.all()
    result = [{'label': f'{r[0]} months', 'value': r[1]} for r in results]
```

## Accessing the Dashboard

1. **From Landing Page**: Select your university → Click "Program Health"
2. **Direct URL**: `/analytics?university=YourUniversityID`
3. **All Universities**: `/analytics` (no filter)

## Tips for Effective Analysis

1. **Start Broad, Then Filter**: Begin with all data, then narrow down
2. **Compare Across Time**: Use the same settings periodically to track trends
3. **Look for Outliers**: Unusual values often indicate issues or opportunities
4. **Cross-Reference**: Use multiple metrics to validate insights
5. **Share Findings**: Export charts (screenshot) for reports and presentations

## Support

For questions or feature requests, please contact your FRAMES administrator or submit an issue to the project repository.
