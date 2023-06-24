import { Fragment, useEffect, useState } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import {
    CalendarIcon,
    BuildingOfficeIcon,
    FlagIcon,
    StarIcon,
    UsersIcon,
    XMarkIcon,
} from '@heroicons/react/24/outline'
import { useStore } from '../store'
import { Link, Route } from "wouter";
import { ToiletIcon } from "./icons.jsx"

const navigation = [
    { name: 'Buildings', href: '/buildings', icon: BuildingOfficeIcon },
    { name: 'Amenities', href: '/amenities', icon: FlagIcon },
    { name: 'Ratings', href: '/ratings', icon: StarIcon },
]

const userNavigation = [
    { name: 'Your Profile', href: '#' },
    { name: 'Settings', href: '#' },
    { name: 'Sign out', href: '#' },
]

function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
}

export default function Navigation() {

    const [location, setLocation] = useState("/");

    const [
        sidebarOpen,
        setSidebarOpen
    ] = useStore(state => [
        state.sidebarOpen,
        state.setSidebarOpen
    ]);

    useEffect(() => {
        setLocation(window.location.pathname);
    }, [window.location.pathname]);

    return (<Fragment>

        {/* Mobile Bar */}
        <Transition.Root show={sidebarOpen} as={Fragment}>
            <Dialog as="div" className="relative z-40 lg:hidden" onClose={setSidebarOpen}>
                <Transition.Child
                    as={Fragment}
                    enter="transition-opacity ease-linear duration-300"
                    enterFrom="opacity-0"
                    enterTo="opacity-100"
                    leave="transition-opacity ease-linear duration-300"
                    leaveFrom="opacity-100"
                    leaveTo="opacity-0"
                >
                    <div className="fixed inset-0 bg-gray-600 bg-opacity-75" />
                </Transition.Child>

                <div className="fixed inset-0 z-40 flex">
                    <Transition.Child
                        as={Fragment}
                        enter="transition ease-in-out duration-300 transform"
                        enterFrom="-translate-x-full"
                        enterTo="translate-x-0"
                        leave="transition ease-in-out duration-300 transform"
                        leaveFrom="translate-x-0"
                        leaveTo="-translate-x-full"
                    >
                        <Dialog.Panel className="relative flex w-full max-w-xs flex-1 flex-col bg-indigo-700 pt-5 pb-4">
                            <Transition.Child
                                as={Fragment}
                                enter="ease-in-out duration-300"
                                enterFrom="opacity-0"
                                enterTo="opacity-100"
                                leave="ease-in-out duration-300"
                                leaveFrom="opacity-100"
                                leaveTo="opacity-0"
                            >
                                <div className="absolute top-0 right-0 -mr-12 pt-2">
                                    <button
                                        type="button"
                                        className="ml-1 flex h-10 w-10 items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                                        onClick={() => setSidebarOpen(false)}
                                    >
                                        <span className="sr-only">Close sidebar</span>
                                        <XMarkIcon className="h-6 w-6 text-white" aria-hidden="true" />
                                    </button>
                                </div>
                            </Transition.Child>
                            <div className="flex flex-shrink-0 items-center px-4">
                                <img
                                    className="h-8 w-auto"
                                    src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=300"
                                    alt="Your Company"
                                />
                            </div>
                            <div className="mt-5 h-0 flex-1 overflow-y-auto">
                                <nav className="space-y-1 px-2">
                                    {navigation.map((item) => {
                                        return <a
                                            key={item.name}
                                            href={item.href}
                                            className={classNames(
                                                location.includes(item.href) ? 'bg-indigo-800 text-white' : 'text-indigo-100 hover:bg-indigo-600',
                                                'group flex items-center rounded-md px-2 py-2 text-base font-medium'
                                            )}
                                        >
                                            <item.icon className="mr-4 h-6 w-6 flex-shrink-0 text-indigo-300" aria-hidden="true" />
                                            {item.name}
                                        </a>
                                    })}
                                </nav>
                            </div>
                        </Dialog.Panel>
                    </Transition.Child>
                    <div className="w-14 flex-shrink-0" aria-hidden="true">
                        {/* Dummy element to force sidebar to shrink to fit close icon */}
                    </div>
                </div>
            </Dialog>
        </Transition.Root>

        {/* Static sidebar for desktop */}
        <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
            {/* Sidebar component, swap this element with another sidebar if you like */}
            <div className="flex flex-grow flex-col overflow-y-auto bg-indigo-700 pt-5">
                <div className="flex flex-shrink-0 items-center px-4">
                    <div className="text-white ">
                        <div className="inline-block fill-current h-auto w-8 mr-3"><ToiletIcon /></div>
                        <span className="font-medium text-xl" style={{ verticalAlign: "middle" }}>OpenToilet</span>
                    </div>
                </div>
                <div className="mt-5 flex flex-1 flex-col">
                    <nav className="flex-1 space-y-1 px-2 pb-4">
                        {navigation.map((item) => (
                            <Link key={item.name} to={item.href}>
                                <a
                                    href="#"
                                    className={classNames(
                                        location.includes(item.href) ? 'bg-indigo-800 text-white' : 'text-indigo-100 hover:bg-indigo-600',
                                        'group flex items-center rounded-md px-2 py-2 text-sm font-medium'
                                    )}
                                >
                                    <item.icon className="mr-3 h-6 w-6 flex-shrink-0 text-indigo-300" aria-hidden="true" />
                                    {item.name}
                                </a>
                            </Link>
                        ))}
                    </nav>
                </div>
            </div>
        </div>
    </Fragment>

    )
}
