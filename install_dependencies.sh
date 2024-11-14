#!/bin/bash
for service in */ ; do
    if [ -f "$service/pom.xml" ]; then
        echo "Installing dependencies for $service"
        (cd "$service" && mvn install)
    elif [ -f "$service/build.gradle" ]; then
        echo "Building $service with Gradle"
        (cd "$service" && gradle build)
    fi
done

