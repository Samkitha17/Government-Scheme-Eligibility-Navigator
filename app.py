from flask import Flask, render_template, request
from schemes import schemes

app = Flask(__name__)


# ==========================================
# FIRST PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# SECOND PAGE - PROFILE
# ==========================================

@app.route("/profile", methods=["POST"])
def profile():

    category = request.form.get("category")

    return render_template(
        "profile.html",
        category=category
    )


# ==========================================
# FIND SCHEMES
# ==========================================

@app.route("/find-schemes", methods=["POST"])
def find_schemes():

    category = request.form.get("category")

    age = int(request.form.get("age"))

    income = request.form.get("income")

    state = request.form.get("state")

    gender = request.form.get("gender")

    recommendations = []


    # Check all schemes

    for scheme in schemes:

        score = 0

        reasons = []


        # CATEGORY

        if scheme["category"] == category:

            score += 40

            reasons.append(
                "Your profile category matches."
            )


        # AGE

        if scheme["min_age"] <= age <= scheme["max_age"]:

            score += 20

            reasons.append(
                "Your age matches."
            )


        # INCOME

        if income in scheme["income"]:

            score += 20

            reasons.append(
                "Your income matches."
            )


        # STATE

        if (
            "All" in scheme["states"]
            or state in scheme["states"]
        ):

            score += 10

            reasons.append(
                "Your state matches."
            )


        # GENDER

        if (
            "All" in scheme["gender"]
            or gender in scheme["gender"]
        ):

            score += 10

            reasons.append(
                "Your gender matches."
            )


        # ADD SCHEME

        if score >= 40:

            if score >= 80:

                status = "Eligible"

            elif score >= 60:

                status = "Potentially Eligible"

            else:

                status = "Needs Verification"


            recommendations.append({

                "name": scheme["name"],

                "score": score,

                "status": status,

                "benefit": scheme["benefit"],

                "documents": scheme["documents"],

                "reasons": reasons

            })


    # Sort by highest score

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return render_template(

        "result.html",

        category=category,

        age=age,

        income=income,

        state=state,

        gender=gender,

        recommendations=recommendations

    )


# ==========================================
# SCHEME PASSPORT
# ==========================================

@app.route("/passport", methods=["POST"])
def passport():

    category = request.form.get("category")

    age = int(request.form.get("age"))

    state = request.form.get("state")

    gender = request.form.get("gender")


    recommendations = []


    # Check schemes

    for scheme in schemes:

        score = 0


        # CATEGORY

        if scheme["category"] == category:

            score += 40


        # AGE

        if scheme["min_age"] <= age <= scheme["max_age"]:

            score += 20


        # STATE

        if (
            "All" in scheme["states"]
            or state in scheme["states"]
        ):

            score += 10


        # GENDER

        if (
            "All" in scheme["gender"]
            or gender in scheme["gender"]
        ):

            score += 10


        # ADD MATCHING SCHEME

        if score >= 40:

            if score >= 80:

                status = "Eligible"

            else:

                status = "Potentially Eligible"


            recommendations.append({

                "name": scheme["name"],

                "score": score,

                "status": status,

                "benefit": scheme["benefit"]

            })


    # Sort schemes

    recommendations.sort(

        key=lambda x: x["score"],

        reverse=True

    )


    # TOTAL SCHEMES

    total_schemes = len(recommendations)


    # ELIGIBLE COUNT

    eligible_count = len([

        scheme

        for scheme in recommendations

        if scheme["status"] == "Eligible"

    ])


    # POTENTIAL COUNT

    potential_count = len([

        scheme

        for scheme in recommendations

        if scheme["status"] == "Potentially Eligible"

    ])


    # OPEN PASSPORT PAGE

    return render_template(

        "passport.html",

        category=category,

        age=age,

        state=state,

        gender=gender,

        recommendations=recommendations,

        total_schemes=total_schemes,

        eligible_count=eligible_count,

        potential_count=potential_count

    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)