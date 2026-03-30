#!/usr/bin/env bash
set -euo pipefail

BASEDIR="$(cd "$(dirname "$0")" && pwd)"

case "${1:-}" in
    update)
        echo "Moving the files to their place"
        echo
        echo "Scripts -> /usr/local/bin/"
        echo "Services -> /etc/systemd/system/"

        # Copy scripts
        if compgen -G "$BASEDIR/scripts/*" > /dev/null; then
            sudo chmod +x "$BASEDIR"/scripts/*
            sudo cp -r "$BASEDIR"/scripts/* /usr/local/bin/
        fi

        # Copy services (recursive)
        for service in "$BASEDIR"/services/*/*.service; do
            [ -e "$service" ] || continue
            sudo cp "$service" /etc/systemd/system/
        done

        # Copy web server files
        sudo cp -r /home/advent/Fieldrich_Gateway_V2/server/ /var/www/gateway

        sudo systemctl daemon-reload
    ;;

    restart)
        echo "Restarting enabled services..."
        echo

        for service in "$BASEDIR"/services/*/*.service; do
            [ -e "$service" ] || continue
            service_name="$(basename "$service")"

            if systemctl is-enabled --quiet "$service_name"; then
                echo "Restarting $service_name"
                sudo systemctl restart "$service_name"
            else
                echo "Skipping $service_name (not enabled)"
            fi
        done
    ;;

    enable)
        echo "Enabling all services..."
        echo

        for service in "$BASEDIR"/services/*/*.service; do
            [ -e "$service" ] || continue
            service_name="$(basename "$service")"

            echo "Enabling $service_name"
            sudo systemctl enable "$service_name"
        done
    ;;

    disable)
        echo "Disabling all services..."
        echo

        for service in "$BASEDIR"/services/*/*.service; do
            [ -e "$service" ] || continue
            service_name="$(basename "$service")"

            echo "Disabling $service_name"
            sudo systemctl disable --now "$service_name" || true
        done
    ;;

    remove)
        echo "Removing all services and scripts..."
        echo

        # Disable + remove services
        for service in "$BASEDIR"/services/*/*.service; do
            [ -e "$service" ] || continue
            service_name="$(basename "$service")"

            sudo systemctl disable --now "$service_name" || true

            if [[ -f "/etc/systemd/system/$service_name" ]]; then
                sudo rm -f "/etc/systemd/system/$service_name"
                echo "$service_name removed"
            fi
        done

        # Remove scripts
        for script in "$BASEDIR"/scripts/*; do
            [ -e "$script" ] || continue
            script_name="$(basename "$script")"

            if [[ -f "/usr/local/bin/$script_name" ]]; then
                sudo rm -f "/usr/local/bin/$script_name"
                echo "$script_name removed"
            fi
        done

        sudo systemctl daemon-reload
    ;;

    *)
        echo "Usage: $0 {update|enable|disable|restart|remove}"
        exit 1
    ;;
esac
